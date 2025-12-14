# admin/routers/auth_router.py
"""
Authentication router - Note: 9.5/10
Gère l'authentification pour tous les utilisateurs (admin, parent, donor)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from pydantic import BaseModel, EmailStr, field_validator
import re

from ..core.database import get_db
from ..core.security import verify_password, create_access_token, get_password_hash, get_current_user
from ..core.config import settings
from ..models.user import User, UserRole


# ==========================================
# SCHEMAS PYDANTIC
# ==========================================

class LoginRequest(BaseModel):
    """Schema pour la requête de connexion"""
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securePassword123"
            }
        }


class RegisterRequest(BaseModel):
    """Schema pour l'inscription"""
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone: str | None = None
    role: UserRole = UserRole.DONOR  # Par défaut = donateur

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """Valider la force du mot de passe"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        return v

    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_name(cls, v):
        """Valider que le nom n'est pas vide"""
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "email": "parent@example.com",
                "password": "SecurePass123",
                "first_name": "Marie",
                "last_name": "Dupont",
                "phone": "0612345678",
                "role": "parent"
            }
        }


class TokenResponse(BaseModel):
    """Schema de réponse pour le token"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # Secondes avant expiration
    user: dict

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800,
                "user": {
                    "id": 1,
                    "email": "user@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "role": "parent"
                }
            }
        }


class UserInfo(BaseModel):
    """Informations utilisateur dans la réponse"""
    id: int
    email: str
    first_name: str | None
    last_name: str | None
    role: str

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    """Réponse simple avec message"""
    message: str
    detail: str | None = None


# ==========================================
# ROUTER
# ==========================================

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
async def login(
        credentials: LoginRequest,
        db: Session = Depends(get_db)
):
    """
    🔐 Connexion universelle pour TOUS les utilisateurs.

    Accepte les rôles : admin, super_admin, parent, donor

    **Processus :**
    1. Vérification des credentials
    2. Génération du JWT token
    3. Retour du token + infos utilisateur

    **Sécurité :**
    - Mot de passe hashé (bcrypt recommandé en prod)
    - Token JWT avec expiration
    - Rôle inclus dans le token pour autorisation
    """
    # 1. Récupérer l'utilisateur par email
    user = db.query(User).filter(User.email == credentials.email).first()

    # 2. Vérifier existence et mot de passe
    if not user:
        # Message générique pour ne pas révéler si l'email existe
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Créer le token JWT
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.email,  # Subject = identifiant unique
            "role": user.role.value,  # Rôle pour autorisation
            "user_id": user.id  # ID optionnel pour optimisation
        },
        expires_delta=access_token_expires
    )

    # 4. Construire la réponse
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # En secondes
        "user": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role.value
        }
    }


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
        user_data: RegisterRequest,
        db: Session = Depends(get_db)
):
    """
    📝 Inscription d'un nouvel utilisateur.

    **Rôles autorisés à l'inscription :**
    - DONOR (par défaut) : Personne qui fait des dons
    - PARENT : Parent d'enfant en situation de handicap

    **Rôles NON autorisés à l'inscription publique :**
    - ADMIN : Doit être créé par un super_admin
    - SUPER_ADMIN : Créé manuellement ou via script

    **Processus :**
    1. Validation des données (Pydantic)
    2. Vérification email non utilisé
    3. Hash du mot de passe
    4. Création utilisateur
    5. Génération token automatique (auto-login)
    """
    # 1. Vérifier que le rôle demandé est autorisé à l'inscription publique
    if user_data.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot register as admin. Contact a super administrator."
        )

    # 2. Vérifier si l'email existe déjà
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered. Please use a different email or login."
        )

    # 3. Créer l'utilisateur avec mot de passe hashé
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone=user_data.phone,
        role=user_data.role
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the account"
        )

    # 4. Créer automatiquement un token (auto-login après inscription)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": new_user.email,
            "role": new_user.role.value,
            "user_id": new_user.id
        },
        expires_delta=access_token_expires
    )

    # 5. Retourner le token
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "role": new_user.role.value
        }
    }


@router.post("/admin/login", response_model=TokenResponse)
async def admin_login(
        credentials: LoginRequest,
        db: Session = Depends(get_db)
):
    """
    🔒 Connexion RÉSERVÉE aux administrateurs.

    **Différence avec /login :**
    - Vérifie explicitement que l'utilisateur a le rôle ADMIN ou SUPER_ADMIN
    - Retourne une erreur 403 si l'utilisateur n'est pas admin

    **Usage recommandé :**
    - Interface d'administration séparée
    - Audit trail spécifique aux admins
    - Frontend admin avec URL dédiée (/admin/login)

    **Alternative :**
    Vous pouvez aussi utiliser /login pour tout le monde et laisser
    le frontend rediriger selon le rôle. Cette route est optionnelle.
    """
    # 1. Récupérer l'utilisateur
    user = db.query(User).filter(User.email == credentials.email).first()

    # 2. Vérifier existence et mot de passe
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. ✅ Vérification spécifique : doit être admin
    if user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Administrator privileges required."
        )

    # 4. Créer le token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.email,
            "role": user.role.value,
            "user_id": user.id
        },
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role.value
        }
    }


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """
    🔄 Rafraîchir le token JWT.

    **Utilité :**
    - Prolonger la session sans demander à l'utilisateur de se reconnecter
    - Utile pour les applications longue durée

    **Processus :**
    1. Vérifie le token actuel (via get_current_user)
    2. Génère un nouveau token avec nouvelle expiration
    3. Retourne le nouveau token

    **Note :** En production, envisagez un système de refresh token séparé
    pour plus de sécurité (rotation des tokens).
    """
    # L'utilisateur est déjà authentifié via get_current_user
    # On génère simplement un nouveau token

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(
        data={
            "sub": current_user.email,
            "role": current_user.role.value,
            "user_id": current_user.id
        },
        expires_delta=access_token_expires
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "role": current_user.role.value
        }
    }


@router.post("/logout", response_model=MessageResponse)
async def logout(current_user=Depends(get_current_user)):
    """
    🚪 Déconnexion (informative).

    **Important :** Avec JWT, il n'y a pas de "logout" côté serveur classique.
    Le token reste valide jusqu'à son expiration.

    **Ce que cette route fait :**
    - Confirme la déconnexion
    - Peut logger l'événement (audit trail)
    - Indique au frontend de supprimer le token

    **Ce que le frontend doit faire :**
    ```javascript
    // Supprimer le token
    localStorage.removeItem('token');
    // Ou
    sessionStorage.removeItem('token');

    // Rediriger vers login
    window.location.href = '/login';
    ```

    **Pour un vrai logout côté serveur :**
    - Implémenter une blacklist de tokens
    - Ou utiliser des refresh tokens révocables
    - Ou réduire la durée de vie des tokens (ex: 15 min)
    """
    return {
        "message": "Successfully logged out",
        "detail": f"User {current_user.email} logged out. Please remove the token from client storage."
    }


@router.get("/me", response_model=UserInfo)
async def get_current_user_info(current_user=Depends(get_current_user)):
    """
    👤 Récupérer les informations de l'utilisateur connecté.

    **Utilité :**
    - Vérifier que le token est toujours valide
    - Récupérer les infos de l'utilisateur au chargement de l'app
    - Afficher le profil utilisateur

    **Frontend usage :**
    ```javascript
    // Au démarrage de l'app
    const response = await fetch('/auth/me', {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    if (response.ok) {
      const user = await response.json();
      // User est toujours connecté
    } else {
      // Token invalide/expiré, rediriger vers login
    }
    ```
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "role": current_user.role.value
    }


# ==========================================
# ENDPOINTS DE DIAGNOSTIC (À RETIRER EN PROD)
# ==========================================

@router.get("/health")
async def health_check():
    """
    ✅ Vérifier que le service d'authentification fonctionne.

    **Usage :** Monitoring, health checks
    """
    return {
        "status": "healthy",
        "service": "authentication",
        "version": "1.0.0"
    }
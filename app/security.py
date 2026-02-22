from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from app.config import settings
import hashlib
import bcrypt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha em texto plano corresponde ao hash."""
    # O hash no banco pode estar em string, bcrypt precisa de bytes
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    
    pwd_bytes = _prepare_password(plain_password)
    return bcrypt.checkpw(pwd_bytes, hashed_password)

def get_password_hash(password: str) -> str:
    """Gera o hash da senha usando bcrypt. Trata senhas longas."""
    pwd_bytes = _prepare_password(password)
    # Gera o salt e o hash
    return bcrypt.hashpw(pwd_bytes, bcrypt.gensalt()).decode('utf-8')

def _prepare_password(password: str) -> bytes:
    """Prepara a senha para o bcrypt (limite de 72 bytes)."""
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 70:
        # Usa o hexdigest do SHA256 (64 bytes) se for muito longa
        # Hexdigest retorna string, então codificamos para ascii/utf-8 novamente
        return hashlib.sha256(password_bytes).hexdigest().encode('utf-8')
    return password_bytes

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria um token JWT de acesso."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

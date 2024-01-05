from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    """Klasa za hashanje passworda. Samo naglasak zasto klasa nema konstruktor
    nego samo static metode, je to sto ne bi imalo smisla stvarati objekt nad
    kojem bi se provjeravala dva passworda, kada mozemo imati samo
    funkciju za to. No razlog zasto je klasa uopce napravljena, je to sto ce
    kroz kod biti lakse razmjeti za sto se koristi funkcija i odakle dolazi.
    """

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

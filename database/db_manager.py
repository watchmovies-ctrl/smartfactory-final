import firebase_admin
from firebase_admin import credentials, firestore
import os

# GLOBAL DB VARIABLE
db = None

def init_firebase():
    global db
    
    # If db is already set, return it immediately
    if db is not None:
        return db

    # Check if Firebase app is already initialized to avoid "App already exists" error
    try:
        if not firebase_admin._apps:
            # --- HARDCODED CREDENTIALS FOR VERCEL ---
            cred_dict = {
                "type": "service_account",
                "project_id": "smartfactory-bea6c",
                "private_key_id": "0d69946a455381674291aefd177a0c9e34fe85dc",
                "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCsVNKk3GgHOA44\nWpAfpcO6U2VituG4RsBSqQ+OWz7SDas4YE0+bOn/fwR7EIQmd6dhZTp5og1lj97c\nBwPNkFz6f3g3Aa74LtqoUMclKOQQ+GLkrZqeFNHop9njXBn+SoJieet+8gqLbTqT\n4sMsra64b37BRnzT6D/hBUogO43SavVdlvW8Lz3RcZ78Ivgxmr03x6wxHul7UrNj\nNAWNaebV6QfN0YbE4cxHydxJ3n3arL9/b0+wupwjveelZVjqcUYub7RMK5/rr479\ndRYGj0lbWr3D3IQkaFEIzCMMVIAVZRbScqBHdIn2Ucg19JT9QVpCDdudkUr4473J\nA4wiLjNNAgMBAAECggEADPCdlIV8RjZ+UtryAX5X8RC8ByqGTmj5nftV0LGnSOx/\n087fXfWdqHKoKnl2AtFvPw/z0RhK+zpPWKQqM/BIGwMhSrgUpEwYXRUbrv2gCmos\nOtGST5ZuoJKh+MF8rix4F97hwPl5szhzcpFPaHZuLSkqEmcxjlPdIA9enob6Qjdo\nM5MUvGOxqEEurUMmtzoSVNtYU5vde96eYQ405RCyha+5V8uNr7t2C1TczHwc1Cqw\niIAm/CY9D4j8pplLGy7OKdiYRDKf9Ejbigpa1cxXySuQv4lC+B8AWfOaSDmGprWa\nYovAjoTg/dn4NFrDUuv2jea/jIX1aMg9ZH6KTIQPYQKBgQDf69V8AtGvroDj+zhK\nU7vLBl0915jWEz3Jb3iNphEWAVbymZfa7GEYETR9oeKHgHSeLYj3iCSm8NxTmIUj\n0h16lNarlxxsv2MHZvjTe/pIyM1VzfS4oXj1Kq4yTTrcisd9evD0HSNIGPasr9FD\nz0KyyOTVXa1iJloplXblX+h1dQKBgQDFBPaS4NPnGMCdHq6loKbxABBRysP6I0BW\n2djPs93OKELaFH9NuSA3AdaL5a/WgB3FSIALQSDlwpA00dV0RuQ+A67gm/A9Knzr\nUbfHjbGwHq5kavROU6YJDRhcpiO8z9f2dA84Ccfx3nNLeKp8omepZ7eX2EnFnfYj\nvmZFHFsTeQKBgHjnY5vUAdg0BtASQzCOyaUzyICtuo5MUV5EW/lPo4YYLxRKrl28\nqChQkeEL2b6EM3N87qmIzxF8l9pjTfArcVNQriB0NRras+O5S70VAezuzz/3Np3C\nQgdOhkQOwyt1m4U7LoMAgJ5bLEXNoNZWQJM8OaKjNAz83E37r/jlsiRJAoGAPiE5\njMn/qQHiQ+oYEz0dSCTIALMbqDcTpA/g0mcbTFbf9hu+pYj6wr3+pXFSSSdvu/YI\nAwSP1kTL6ww87wUoFvJcZJJoaTGL4T2M4g4p+atDPYGI92ZjlrkddKIj5Pf6V8rz\nva0/82M+Io+z28fvPrnpaKYZZYtRwqXZZHPzuKkCgYBpBbkVUs9AQV6lrALAvBvV\nCKajVx7kIkDrR6toZNBv6rI8zIdSNU5lSZJvxgXr0MbXaIBFTsb4SAjq3yFjgO+p\nmIF3ExcHE5FVh47GR3cAJ6hJ/kOQvCyGNEsMt38scECo4WTtsk6ZHDCrEjwY9iMM\nTtk0yy96nfVGLavOH+dcDQ==\n-----END PRIVATE KEY-----\n",
                "client_email": "firebase-adminsdk-fbsvc@smartfactory-bea6c.iam.gserviceaccount.com",
                "client_id": "108887982971099034099",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40smartfactory-bea6c.iam.gserviceaccount.com",
                "universe_domain": "googleapis.com"
            }

            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            print("✅ Firebase Initialized New App")
        else:
            print("⚠️ Firebase App Already Existed - Reusing")
        
        db = firestore.client()
        return db

    except Exception as e:
        print(f"❌ Firebase Critical Error: {e}")
        return None

from configparser import ConfigParser
from cryptography.fernet import Fernet

from configs import settings



def initconfig(env):
    file = "configs/app.config"
    configs = ConfigParser()
    configs.read(file)

    # Database Creds
    settings.db_host = configs[env]['mongodb_host']
    settings.db_password = configs[env]['mongodb_password']
    settings.db_name = configs[env]['mongodb_name']
    settings.db_user = configs[env]['mongodb_user']
    settings.db_port = configs[env]['mongodb_port']
    settings.jwt_secret_key = configs[env]['jwt_secret_key']
    settings.base_media_url = configs[env]['base_media_url']
    settings.smtp_port = configs[env]['smtp_port']
    settings.smtp_server = configs[env]['smtp_server']
    settings.mail_login = configs[env]['mail_login']
    settings.mail_password = configs[env]['mail_password']
    settings.mail_sender = configs[env]['mail_sender']
    settings.verification_url = configs[env]['verification_url']
    settings.encryption_key= Fernet.generate_key()
    settings.url_validity_period= configs[env]['url_validity_period']

    
    
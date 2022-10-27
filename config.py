from environs import Env

env = Env()
env.read_env()  # read .env file, if it exists

TOKEN = env.str('TOKEN')
ADMIN_ID = env.int('ADMIN_ID')

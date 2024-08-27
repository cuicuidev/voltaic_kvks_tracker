from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import streamlit as st

from routes import tracking, progress

class MongoDatabaseHandler:

    def __init__(self, client: MongoClient) -> None:
        self._client = client

        self._db = client.database

        self.benchmarks = self._db.benchmarks
        self.users = self._db.users

@st.cache_resource
def get_client(uri) -> MongoClient:
    return MongoClient(host=uri, server_api=ServerApi("1"))

def main() -> None:
    user = st.secrets.get("MONGO_USER")
    passwd = st.secrets.get("MONGO_PASSWD")
    cluster = st.secrets.get("MONGO_CLUSTER")
    code = st.secrets.get("MONGO_CODE")

    if any([user is None, passwd is None, cluster is None, code is None]):
        raise Exception("a44: error de conexión a la base de datos.")

    uri = f"mongodb+srv://{user}:{passwd}@{cluster.lower()}.{code}.mongodb.net/?retryWrites=true&w=majority&appName={cluster}"
    db = MongoDatabaseHandler(get_client(uri))

    st.write("# Voltaic")
    track, prog = st.tabs(["Tracking", "Progress"])

    ###########################################
    tracking.run(anchor=track, db=db)
    ###################################################
    progress.run(anchor=prog, db=db)

if __name__ == "__main__":
    main()

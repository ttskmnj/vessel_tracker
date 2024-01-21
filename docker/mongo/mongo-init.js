db = db.getSiblingDB(process.env.MONGO_INITDB_DATABASE);

db.createCollection(process.env.MONGO_COLLECTION);

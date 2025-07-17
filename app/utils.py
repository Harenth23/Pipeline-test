
def normalize_mongo_document(doc):
    """Convert _id to string id in MongoDB documents."""
    if "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc

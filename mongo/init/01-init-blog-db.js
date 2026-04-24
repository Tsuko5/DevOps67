db = db.getSiblingDB("blog_db");

if (!db.getCollectionNames().includes("posts")) {
  db.createCollection("posts");
}

db.runCommand({
  collMod: "posts",
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["titre", "auteur", "vues"],
      properties: {
        _id: { bsonType: "objectId" },
        titre: { bsonType: "string", minLength: 3 },
        auteur: { bsonType: "string", minLength: 2 },
        vues: { bsonType: "int", minimum: 0 },
        contenu: { bsonType: "string" },
      },
      additionalProperties: false,
    },
  },
});

if (db.posts.countDocuments() === 0) {
  db.posts.insertMany([
    { titre: "Post 1", auteur: "Ugo", vues: NumberInt(20), contenu: "Contenu 1" },
    { titre: "Post 2", auteur: "Damien", vues: NumberInt(40), contenu: "Contenu 2" },
    { titre: "Post 3", auteur: "Evan", vues: NumberInt(60), contenu: "Contenu 3" },
    { titre: "Post 4", auteur: "Frederic", vues: NumberInt(80), contenu: "Contenu 4" },
    { titre: "Post 5", auteur: "Glenden", vues: NumberInt(100), contenu: "Contenu 5" },
  ]);
}

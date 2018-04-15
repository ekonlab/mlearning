use flights_db

// drop inherited temp collections
db.icao_values.drop()
db.oaci_subset.drop()

// delete old ICAO fields from main collection
db.all_points.update(
  { ICAO: { $exists: true }},
  { $unset: { ICAO: "", ICAOVAL: "" }},
    {multi: true} // config object
)

// find all docs with OACI key and OACI value length greather than 3
db.all_points.find(
    { ICAO: { $exists: true }},
    { $expr: { $gt: [{ $strLenCP: "$ICAO" }, 3] }}
)

// create a subset with docs with oaci key
db.all_points.aggregate([
  { $match: { OACI: { $exists: true }}},
  { $project: { OACI: 1 }},
  { $out: "oaci_subset" }
])

// remove from subset all oaci values with less lenght than 3
db.oaci_subset.delete(
  { $expr: { $lt: [{ $strLenCP: "$OACI" }, 3]}}
)

// get a collection with origin ids and splitted OACI values
db.oaci_subset.aggregate([
  { $project: { ICAO: { $substr: [ "$OACI", 0, 3 ]}}},
  { $out: "icao_values" }
})

// update main table with new splitted codes
db.all_points.aggregate([
  { $lookup: { 
    from: "icao_values",
    localField: "_id",
    foreignField: "_id",
    as: "icao_matches"
  }},
  { $replaceRoot: { 
    newRoot: { 
      $mergeObjects: [{ $arrayElemAt: [ "$icao_matches", 0 ]}, "$$ROOT" ]
    }
  }},
  { $project: { icao_matches: 0 }},
  { $out: "all_points" }
])

// get public ICAO values as array
icaos = icao_codes.map((d) => d.ICAO)

// filter suspect flights
db.all_points.aggregate([
  { $match: { ICAO: { $nin: icaos }}},
  { $out: "suspects" }
])

// try to group points by flight id
db.all_points.aggregate([
  { $group: { 
    _id: "$flight_id", 
    count: { $sum: 1 },
    lng: { $push: lng },
    timestamp: { $push: timestamp },
    lat: { $push: lat },
    // HABLAR CON ALBERTO
  }}
])


// output the collection to a json

mongodump --host 127.0.0.1 --port 27017 --db flights_db --collection suspects --archive suspects.bson
bsondump --outFile suspects.json suspects.bson

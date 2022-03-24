const Cloudant = require('@cloudant/cloudant');
async function main(params) {
    let databaseName = "dealerships"
    const client = Cloudant({
        url: params.COUCH_URL,
        plugins: {
            iamauth: {
                iamApiKey: params.IAM_API_KEY
            }
        }
    });

    try {
        let db = client.db.use(databaseName);
        if (params.hasOwnProperty('STATE') || params.hasOwnProperty('state')) {
            let state = params.STATE || params.state;
            let docs = await db.find({
                selector: {
                    "st": {
                        "$eq": state
                    }
                }
            }).then(x => {
                return x.docs;
            });
            if (docs.length > 0) {
                return {
                    "statusCode": 200,
                    "body": docs
                };
            }
            return {
                "statusCode": 404,
                "body": "The state does not exist"
            };
        } else {
            let docs = await db.list({
                include_docs: true
            }).then(x => {
                if (x.rows.length > 0) {
                    return x.rows.map(x => x.doc);
                }
            });
            if (docs.length > 0) {
                return {
                    "statusCode": 200,
                    "body": docs
                };
            }
            return {
                "statusCode": 404,
                "body": "The database is empty"
            };
        }

    } catch (error) {
        return {
            "statusCode": 500,
            "body": error.description
        }
    }
}
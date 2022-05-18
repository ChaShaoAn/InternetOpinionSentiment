const fs = require('fs');


function loadCFG(){
    let rawdata = fs.readFileSync('cfg/db_cfg.json');
    return JSON.parse(rawdata);
}

function makeReturnTemplate(){
    return {
        'status': null, // normal | error
        'error_msg': null, // null | str
        'data' : [],
        'query_id': null
    }
}

module.exports = {
    'loadCFG': loadCFG,
    'makeReturnTemplate': makeReturnTemplate
}

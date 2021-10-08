(function process( /*RESTAPIRequest*/ request, /*RESTAPIResponse*/ response) {
    var attachment = new GlideSysAttachment();
    var delAttachment = new GlideSysAttachment();
    var pluginGr = new GlideRecord('sn_agent_asset');
    var attachGr = new GlideRecord('sys_attachment');
    gs.info("PLUGGY-API: got plugin name " + request.body.data.name);
    gs.info("PLUGGY-API: got attachment " + request.body.data.attachment);
    var fileName = request.body.data.name + ".tar.gz";
    gs.info("PLUGGY-API: filename is " + fileName);
    var contentType = "application/gzip";

    // look for an existing record

    pluginGr.addQuery('name', request.body.data.name);
    pluginGr.query();
    // if no record is found, create one
    if (!(pluginGr.hasNext())) {
        gs.info("PLUGGY-API: no plugin matching " + request.body.data.name);
        pluginGr.initialize();
        pluginGr.setValue("name", request.body.data.name);
        pluginGr.setValue('description', request.body.data.name);
        // set the "directory" attribute true so it lets us create the record without having an attachment first
        pluginGr.setValue('directory', true);
        pluginGr.insert();
        gs.info("PLUGGY-API: created new plugin record sys_id " + pluginGr.sys_id);

    }
    // if a record is found, pull it into the GR
    else {
        pluginGr.next();
        gs.info("PLUGGY-API: plugin matching " + request.body.data.name + " has sys_id " + pluginGr.sys_id);
        // delete existing attachment
        attachGr.addEncodedQuery('table_name=sn_agent_asset^table_sys_id=' + pluginGr.sys_id);
        attachGr.query();
        while (attachGr.next()) {
            gs.info("PLUGGY-API: deleting attachment "+attachGr.sys_id);
            delAttachment.deleteAttachment(attachGr.sys_id);
        }
    }
    // add the new attachment
    var addAttGr = attachment.writeBase64(pluginGr, fileName, contentType, request.body.data.attachment);
    pluginGr.setValue('directory', false);
    
    // set optional attributes
    if (request.body.data.hasOwnProperty('os')) {
        gs.info("PLUGGY-API: got os " + request.body.data.os);
        pluginGr.setValue('os',request.body.data.os);
    }
    if (request.body.data.hasOwnProperty('platform')) {
        gs.info("PLUGGY-API: got platform " + request.body.data.platform);
        pluginGr.setValue('platform',request.body.data.platform);
    }
    pluginGr.update();
    //var responseBody={};
    //responseBody.sysId=pluginGr.sys_id;
    //response.setBody(responseBody);
})(request, response);

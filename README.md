ejabberd2openfire
=================

Users migration Python script


A short usage example

    On your server running EJabberD, create a dumpfile using:

ejabberdctl dump ejabberd_dumpfile

 - for this ejabberd should be started from root user (check init scipt)

    BEWARE! The file will turn up in your database path, most probably in '''/var/lib/ejabberd/ejabberd_dumpfile'''.
    Use ejabberd2openfire.py to create a OpenFire import/export XML-File:

cd your_ejabberd2openfire_directory/ && ./ejabberd2openfire.py ejabberd_dump new_import_data.xml

    Now, surf to your OpenFires web-admin-interface, on the user import/export page, e.g.:d

http://YOUR.DOMA.IN:9090/plugins/userimportexport/import-user-data.jsp

 - for this should be installed plugin "User Import Export"

    Import the data. Hopefully everything works. Now enjoy your new OpenFire Installation using your old EJabberd data!

 Source: 
 http://indefero.ghostdub.de/index.php/p/ejabberd2openfire/page/Usage/


 In my case I haven't users in Ejabberd at all (authorization was via another way),
 but that were presents rosters and vCard, I not needed in vCard.

 And this script did not want to do migration only of rosters.
 Therefore script was changed for ability create users from the rosters
 and then assign rosters to their users.

 Usage is identical for previous one, but only use script:

./roster_ejabberd2openfire.py ejabberd_dump new_import_data.xml

Also this script sets empty password, because in roster password not specified,
you may change it in line

    <Roster>"""%(user[0].replace("\\\\","\\"),"YOUR_PASSWORD_FOR_ALL_USERS",int(time.time()), int(time.time())))

Besides was improved migration of user ID, example:
userID, how it see human:
	miami@test.com
userID, how it is in ejabberd dump:
	miami\\test.com
userID, how it should be in xml for import to Openfire:
	miami\40test.com

Therefore I do this replace:
	...user[0].replace("\\\\","\\")...
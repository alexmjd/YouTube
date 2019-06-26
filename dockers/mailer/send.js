var express = require('express');
var bodyParser = require('body-parser');
const cors = require('cors');
var app = express();
const axios = require('axios');
//app.set('port', process.env.PORT || 5005 );
// app.use(cors());
app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS');
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, authorization");
    next();
});
app.use(bodyParser.json());

const MailDev = require('maildev')
const nodemailer = require('nodemailer')
const maildev = new MailDev({
    smtp: 1025 // incoming SMTP port - default is 1025
})
const transport = nodemailer.createTransport({
    port: 1025,
    ignoreTLS: true,
    // other settings...
});

maildev.listen(function(err) {
    console.log('We can now sent emails to port 1025!')
})

function send_mail(type, email)
{
    subject = ""
    body = ""
    switch(type){
        case 'password':
            subject = "Modification mot de passe"
            body = "Votre mot de passe a bien été changé"
            break;
        case 'encoding':
            subject = "encoding video"
            body = "Encoding effectué"
            break;
    }

    var mail = {
        from: "no-reply@yt.com",
        to: email,
        subject: subject,
        html: body
    }
    transport.sendMail(mail, function(error, response){
        if(error){
            console.log("Erreur lors de l'envoie du mail!");
            console.log(error);
        }else{
            console.log("Mail envoyé avec succès!")
        }
        transport.close();
    });
}

app.get('/', function(req, res, next) {
    console.log("ok")
    //send_mail("password", "dy@ot.fr")
    //axios({url: 'http://t_python:5000/videos', method: 'GET'})
    //    .then(resp => {
     //       console.log('add resppppppp', resp.data.data)
     //   })
     //   .catch(err => {
     //       console.log('errrrrrrrrr', err)
     //   })
});

app.get('/ok', function(req, res, next) {
    console.log("c'est relié")
    //send_mail("password", "dy@ot.fr")
    res.send('ok')

});
app.post('/te', function(req, res, next) {
    console.log('cela marche ', res.data.data)
    /* Notre code pour nodemailer */
});
app.use(function(req, res) {
    res.sendStatus(404);
});


// Print new emails to the console as they come in
maildev.on('new', function(email){
    console.log('Received new email with subject: %s', email.subject)
})

// Get all emails
maildev.getAllEmail(function(err, emails){
    if (err) return console.log(err)
    console.log('There are %s emails', emails.length)
})

app.listen(5005, '0.0.0.0', function() {
    console.log('Your node.js server is running on PORT: 5005');
});

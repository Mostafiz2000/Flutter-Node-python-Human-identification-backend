var express = require('express'); 
var bodyParser = require('body-parser'); 
 
var app = express(); 
  
app.use(bodyParser.json()); 
app.use(bodyParser.urlencoded({ extended: false })); 
var a;
var b;
var c;
var fo;
var name;
var option;
var check;


app.post("/postdata", (req, res) => { 

    var foo = req.body.foo; 
    a=foo;
    var kaa = req.body.kaa; 
    b = kaa;
    var ma= req.body.max;
    c= ma;
    
    console.log(kaa); 
    console.log(ma);
    res.send("process complete"); 
}); 
app.post("/sdata", (req, res) => { 

    var fow = req.body.status; 
   fo=fow
   option=req.body.option;
   name=req.body.string;
   check=req.body.check

    
    console.log(fow); 
    
    res.send("process complete"); 
});
app.get("/getsdata", (req, res) => { 

    var data = { // this is the data you're sending back during the GET request 
        data1: fo, 
        option: option,
        str: name,
        op:check
     
    } 
    res.status(200).json(data)
});
 
app.get("/getdata", (req, res) => { 
    var data = { // this is the data you're sending back during the GET request 
        data1: a, 
        data2: b ,
        data3 : c
    } 
    res.status(200).json(data) 
}); 
  
app.listen(4000); 
// app.js
const https = require("https");

const Stream = require("stream").Transform;
const fs = require("fs");
const express = require("express");
 const app = express();
//
 app.get("/", (req, res) => {
  //res.send(`Hello World!`);
  https
  .get("https://2biz8ozb25.execute-api.ap-northeast-1.amazonaws.com/dev/notification", resp => {
              let data = "";

              resp.on("data", chunk => {
                            data += chunk;
                          });

              resp.on("end", () => {
                            //let url = JSON.parse(data).hdurl;
                            res.send("From frontend----" + data);

                          });
            })
  .on("error", err => {
              console.log("Error: " + err.message);
            });
  });
//
 app.listen(80, () => {
   console.log(`Example app listening on port 80!`);

   });

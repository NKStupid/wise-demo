// app.js
const https = require("https");

const Stream = require("stream").Transform;
const fs = require("fs");
const express = require("express");
 const app = express();
//
 app.get("/", (req, res) => {
  res.send(`Hello World!`);
  https
  .get("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY", resp => {
              let data = "";

              resp.on("data", chunk => {
                            data += chunk;
                          });

              resp.on("end", () => {
                            let url = JSON.parse(data).hdurl;
                            console.log(url);

                          });
            })
  .on("error", err => {
              console.log("Error: " + err.message);
            });
  });
//
 app.listen(3000, () => {
   console.log(`Example app listening on port 3000!`);

   });

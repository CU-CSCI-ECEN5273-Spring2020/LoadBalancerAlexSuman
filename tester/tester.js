
const results = document.getElementById("resultBody");
const runButton = document.getElementById("runButton")
const numTests = document.getElementById("numTests");

async function createRequest(count) {

     return new Promise(function(resolve, reject){

               let req = new XMLHttpRequest();

               req.onreadystatechange = function() {
                    if(this.readyState == 4) {
                         if(this.status == 200) {
                              // console.log("Success: " + count);
                              resolve("Yay!");
                         }
                         else if (this.status == 400) {
                              // console.log("Fail!");
                              resolve("Boo!");
                         }
                    }
               }

               req.open("GET", "http://localhost:8081", true);
               req.send();
     })
}

function runTester(runs) {

     let startTime = performance.now();

     let promises = [];

     for(let count = 0; count < runs; count++) {
          promises.push(createRequest(count));
     }

     Promise.all(promises).then(function(){

          let endTime = performance.now();


          let numRuns = document.createElement("td");
          numRuns.innerHTML = runs;

          let totalTime = document.createElement("td");
          totalTime.innerHTML = (endTime - startTime) + " ms"

          let tr = document.createElement("tr");
          tr.append(numRuns);
          tr.append(totalTime);

          results.append(tr);

     }, function(err){

     });
}

runButton.addEventListener("click", function(){
     let runs = numTests.value;

     runTester(runs);
})
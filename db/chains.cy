CREATE (:Product { name: "Product", lat: tan(rand())*100, lon: tan(rand())*100, co2: 200, cost: 100, time: 0 }) FOREACH (r IN range(0,1)| CREATE (:Wholesaler { name:"Wholesaler" + r, cost: round(exp(rand()*3)+20), co2: round(exp(rand()*8)+250), lat: tan(rand())*100, lon: tan(rand())*100, time: round(rand()*5)})) FOREACH (r IN range(0,10)| CREATE (:Retailer { name:"Retailer" + r, cost: round(exp(rand()*3)+20), co2: round(exp(rand()*8)+250), lat: tan(rand())*100, lon: tan(rand())*100, time: 1})) FOREACH (r IN range(0,2)| CREATE (:SupplierA { name:"SupplierA" + r, cost: round(exp(rand()*3)+20), co2: round(exp(rand()*8)+250), lat: tan(rand())*100, lon: tan(rand())*100, time: round(rand()*5)})) FOREACH (r IN range(0,1)| CREATE (:SupplierB { name:"SupplierB" + r, cost: round(exp(rand()*3)+20), co2: round(exp(rand()*8)+250), lat: tan(rand())*100, lon: tan(rand())*100, time: round(rand()*5)})) FOREACH (r IN range(0,5)| CREATE (:RawSupplierA{ name:"RawSupplierA" + r, cost: round(exp(rand()*3)+20), co2: round(exp(rand()*8)+250), lat: tan(rand())*100, lon: tan(rand())*100, time: round(rand()*5)})) FOREACH (r IN range(0,5)| CREATE (:RawSupplierB{ name:"RawSuppplierB" + r, cost: round(exp(rand()*3)+20), co2: round(exp(rand()*8)+250), lat: tan(rand())*100, lon: tan(rand())*100, time: round(rand()*5)}))

MATCH (sa:SupplierA), (p:Product), (w:Wholesaler), (r:Retailer) CREATE UNIQUE (sa)-[:DELIVER]->(p)-[:DELIVER]->(w) -[:DELIVER]->(r) WITH p, sa MATCH (sb:SupplierB) CREATE UNIQUE (sb)-[:DELIVER]->(p) WITH sb, sa MATCH (ra:RawSupplierA), (rb:RawSupplierB) CREATE UNIQUE (ra)-[:DELIVER]->(sa) CREATE UNIQUE (rb)-[:DELIVER]->(sb)

MATCH (a)-[r]-() RETURN a, r

MATCH (a)-[r]->(b) WITH r, a, b, 2 * 6371 * asin(sqrt(haversin(radians(toInt(a.lat) - toInt(b.lat))) + cos(radians(a.lat))* cos(radians(b.lat))* haversin(radians(a.lon - b.lon)))) AS dist SET r.km = round(dist)

MATCH (p:Product)-[r1]->(w)-[r2]->(re:Retailer) WITH distinct(substring(w.name, 10)) AS Num, avg(r1.km + r2.km) AS Average_Distance, sum(r1.km + r2.km) AS Total_Distance RETURN "Wholesaler" + Num AS Wholesaler, Total_Distance, round(Average_Distance) ORDER BY Total_Distancees

MATCH chain=(rs:RawSupplierA)-[r*]->(re:Retailer) WITH reduce(wait = 0, s IN nodes(chain)| wait + s.time) AS waitTime, chain WHERE waitTime < 8 WITH extract(n IN nodes(chain)| n.name) AS SupplyChain, waitTime ORDER BY SupplyChain[1] RETURN SupplyChain, waitTime

MATCH chain=(rs:RawSupplierA)-[r*]->(re:Retailer) WITH reduce(wait = 0, s IN nodes(chain)| wait + s.time) AS waitTime, chain WHERE waitTime < 8 WITH reduce(dist = 0, s IN relationships(chain)| dist + s.km) AS distance, waitTime, chain WHERE distance < 23000 WITH extract(n IN nodes(chain)| n.name) AS SupplyChain RETURN collect(distinct(SupplyChain[1])) AS Supplier, collect(distinct(SupplyChain[0])) AS RawSupplier

MATCH (n) SET n.costR = round(rand()*10) SET n.timeR = round(rand()*10) SET n.wasteR = round(rand()*10)

MATCH chain=(rsB:RawSupplierB)-[r*]->(p:Product)<-[r*]-(rsA:RawSupplierA) WITH reduce(wait = 0, s IN nodes(chain)| wait + s.timeR) AS tRating, reduce(wait = 0, s IN nodes(chain)| wait + s.costR) AS cRating, reduce(wait = 0, s IN nodes(chain)| wait + s.wasteR) AS wRating, chain, p WITH chain, p, ((cRating*0.6) + (wRating*0.2) + (tRating*0.2) ) AS score WITH score, p, extract(n IN nodes(chain)| n.name) AS SupplyChain1 ORDER BY score DESC MATCH chain=(p)-[r*]->(re:Retailer) WITH reduce(wait = 0, s IN nodes(chain)| wait + s.timeR) AS tRating, reduce(wait = 0, s IN nodes(chain)| wait + s.costR) AS cRating, reduce(wait = 0, s IN nodes(chain)| wait + s.wasteR) AS wRating, chain, score, SupplyChain1 WITH chain, SupplyChain1, ((cRating*0.6) + (wRating*0.2) + (tRating*0.2) + score) AS totalScore WITH SupplyChain1, totalScore, extract(n IN nodes(chain)| n.name) AS SupplyChain2 ORDER BY totalScore DESC RETURN SupplyChain2 + SupplyChain1, totalScore LIMIT 1


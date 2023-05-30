const quotes = ['A rose by any other name would smell as sweet.','All that glitters is not gold.',
    'Elementary, my dear Watson.','Go ahead, make my day.','Heres looking at you, kid.','I think therefore']

//haetaan satunnainen quote quotes listalta ja näytetäänse quotePlace p-tagissa
function randomQuote () {
quotePlace.innerHTML = quotes[(Math.floor(Math.random()*quotes.length))]
}


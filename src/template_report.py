template = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width initial-scale=1">
    <title>Collision Anxiety Report</title>
</head>
<body>
    <div> 
        <h3> Top Level Summary for {date_string} </h3>
        <img src='./images/today.png'>
        <p>
        It's a bit crowded up there.
        </p>

        <h3> Explanation.</h3>
        <p> 
            As Douglas Adams once wrote "space is big. Really big. You just won't believe how vastly hugely mind-bogglingly big it is."
            So we might presume that we have loads of places to put satellites.
            But even with two satellites, unless one is following the other on the same exact path, their paths will cross the same point in the sky twice a day.
            Those in the know might raise the point that two planes can be at the same point in the sky, but at different elevations and thus not crash.
            This is true, but how many planes can you have stacked on top of each other so many times before disaster strikes?
        </p>

        <p> 
            The bar chart above is looking at how close a sample of 200 satellites get within each other.
            Starting with satellites that have an orbital period of 90 minutes and getting longer we build our sample of 200 satellites with data provided by 
            <a href="">space track.</a>
            This orbital period corresponds to an elevation of just over 280 km.
            It might seem arbitrary but this is about the elevation the international space station flies at, so it's of some interest to the humans that live there at any given time.
        </p>
        
        <p> 
            The status reports from space track provide enough information to run the standard perturbations model (SGP4) to figure out roughly where a satellite will be in the future.
            Because the interior of the earth is liquid and moving around all the time, and the atmosphere shrinks and grows with the amount of heating the sun is doing, this leads to an uncertainty on the order of a few km.
        </p>
        
        <p> 
            Some ways to contextualize this is the earths circumference is about fourty thousand kilometers, and these orbits are only a bit longer than that, so you could break up the orbit into ten thousand boxes and be pretty sure which box it was in.
            Another way to think of it is that as these satellites are traveling several kilometers a second, we know to within a fraction of a second where these satellites are.
        </p>
        
        <p> 
        </p>
        
        <p> 
            This uncertainty grows over time so we have to constantly update our records of where any orbiting body is.
            But with the up to date data we can project forward in time where the satellite will be.
            Using an sgp4 implementation in python we generate each satellites trajectory over the course of a day.
            By comparing each trajectory with each other trajectory we can find how close they get to one another.
            The bar chart is illustrating how many satellites get within some distance of crashing into another.
            We see that often as much as 10% of the satellites examine get close enough that both satellites are in the same little box of space where we don't know where they are.
            This necessitates course corrections on a regular basis to maintain safe distances from other objects lest we have any more problematic collisions.
        </p>
   </div>

</body>
</html>
'''
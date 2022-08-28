module testObj( RODCOUNT)
{
    for (i = [0:1:RODCOUNT])
        rotate([0,0,i*10])
            translate([0,i,0])
                cylinder(r=1,h=1);
}
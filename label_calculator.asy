import buffer;


//constants
real LABEL_SCALE_FACTOR = 3;
real GAP_THRESHOLD = 75;

//actually draw everything to calculate size
for(path p: paths)
    draw(p);
//calculate radius to look for labels
real rendered_width = max(currentpicture).x - min(currentpicture).x;
real actual_width = max(currentpicture, true).x - min(currentpicture, true).x;
real label_radius = labelmargin(currentpen) * actual_width / rendered_width * LABEL_SCALE_FACTOR;

for(pair pt: points_to_label){
    real[] intersect_dir = {};
    path label_circle = circle(pt, label_radius);
    draw(label_circle, gray); //for easier debugging
    for(path p : paths){
        real[][] ip = intersections(label_circle, p);
        for(real[] x : ip){
            intersect_dir.push(x[0] * 360 / length(label_circle));
        }
    }
    //calculate the maximum gap
    intersect_dir = sort(intersect_dir);
    if(intersect_dir.length == 0){
        write("dir(90)");
        continue;
    }
    intersect_dir.push(intersect_dir[0] + 360);
    real max_gap = 0;
    int argmax = -1;
    for(int j=0; j<intersect_dir.length-1; ++j){
        if(intersect_dir[j+1] - intersect_dir[j] > max_gap){
            max_gap = intersect_dir[j+1] - intersect_dir[j];
            argmax = j;
        }
    }
    //calculate angles and ship out results
    real angle = (intersect_dir[argmax+1] + intersect_dir[argmax])/2;
    int out_angle = ((int) angle) % 360;
    if(out_angle > 180) out_angle = out_angle - 360;
    if(max_gap > GAP_THRESHOLD){
        dot("$O$", pt, dir(out_angle));
        write("dir(" + (string) out_angle + ")");
    }
    else{
        real scale_factor = min(2, GAP_THRESHOLD / max_gap);
        string out_scale_factor = format( "%.2f", scale_factor);
        dot("$O$", pt, scale_factor * dir(out_angle));
        write(out_scale_factor + "*dir(" + (string) out_angle + ")");
    }
}
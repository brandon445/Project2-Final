var dataPoints =[];

function getDataPoints(csv) {
    var dataPoints =csvLines =points =[];
    csvLines = csv.split(/[\r?\n|\r|\n]+/);

    for(var i=0; i < csvLines.length; i++)
        if(csvLines[i].length > 0) {
            points = csvLines[i].split(",");
            dataPoints.push({
                x:parseFloat(points[0]),
                y:parseFloat(points[1])
            });
        }
    return dataPoints;
}
$.get("https://github.com/RHarmer11/Project2_v2/blob/master/result2.csv",function(data) {
    var chart = new CanvasJS.Chart('chartContainer'), {
       
    };
    chart.render(data);
})
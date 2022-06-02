function customGraph(label, value){
    
    const data = {
        labels : label,//year_product.filter(n=>n),
        datasets:[{
            label:'Dataset',
            data:value,
            backgroundColor: [
                'rgb(128,0,128)',
                            'rgb(255, 99, 132)',
                            'rgb(54, 162, 235)',
                            'rgb(46,139,87)'
                            ],
                            borderColor:'white',
                            borderWidth:0.5,
            // hoverBorderWidth:3,
            hoverBorderColor:'#000',
            hoverOffset: 1
        }]
    };
  
    const options = {
        // responsive:false,
        maintainAspectRatio: false,
        plugins: {
            title: {
                display: true,
                text: 'Custom Data ',
                fontSize:'10',
                position:'top',
                font: {
                    size: 10
                },
            },
            // subtitle: {
            //     display: true,
            //     text: '(In Percent)',
            //     font: {
            //             size: 10
            //         },
            //     padding:10
            // },
            legend: {
                display:true,
                position:'right',
                labels: {
                    // This more specific font property overrides the global property
                    font: {
                        size: 8
                    },
                    boxWidth:10,
                    color:'black'
                },
            },
            datalabels:{
               color:'white'
            }
        
        },
        // scales: {
        //     y: {
        //         stacked: false,
        //         grid: {
        //             display: false,
        //             color: "rgba(255,99,132,0.2)"
        //         }
        //     },
        //     x: {
        //     grid: {
        //         display: false
        //         },
        //     },
            // labels: {
            //         // This more specific font property overrides the global property
            //     font: {
            //         size: 14
            //     }
            // }
        // }
  
    }
    const config = {
        type:'bar',
        data:data,
        options:options,
        plugins: [ChartDataLabels]
    }

    var myChart = {}

    var canva = document.getElementById('graph-custom-search')

    
    let chartStatus = Chart.getChart("graph-custom-search"); // <canvas> id
if (chartStatus != undefined) {
  chartStatus.destroy();
}else{
    console.log(chartStatus)
}

    myChart = new Chart(
        canva,// document.getElementById('graph-custom-search'),
        config
      );

    // myChart.update();

    // if(typeof(myChart) === 'object'){
    //     console.log('Kontul')
    // }
    
}


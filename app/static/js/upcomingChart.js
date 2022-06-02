function dailyChartUpcoming(label, value){

    const data = {
        labels : label,//year_product.filter(n=>n),
        datasets:[{
            label:'Posting dataset',
            data:value,
            backgroundColor: [
                'rgb(128,0,128)',
                            'rgb(255, 99, 132)',
                            'rgb(54, 162, 235)',
                            'rgb(46,139,87)',
                            'rgb(255,153,51)',
                            'rgb(51,255,255)',
                            'rgb(255,51,255)',
                            'rgb(204,0,102)'
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
                text: 'Upcoming Data Day',
                fontSize:'10',
                position:'top',
                font: {
                    size: 10
                },
                color:'white'
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
                    color:'white'
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
        type:'doughnut',
        data:data,
        options:options,
        plugins: [ChartDataLabels]
    }
  
    const myChart = new Chart(
      document.getElementById('graph-upcoming-day'),
      config
    );

}

function monthChartUpcoming(label, value){
    
    const data = {
        labels : label,//year_product.filter(n=>n),
        datasets:[{
            label:'Posting dataset',
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
                text: 'Upcoming Data Month',
                fontSize:'10',
                position:'top',
                font: {
                    size: 10
                },
                color:'white'
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
                    color:'white'
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
        type:'doughnut',
        data:data,
        options:options,
        plugins: [ChartDataLabels]
    }
  
    const myChart = new Chart(
      document.getElementById('graph-upcoming-month'),
      config
    );

}

function yearChartUpcoming(label, value){
    const data = {
        labels : label,//year_product.filter(n=>n),
        datasets:[{
            label:'Posting dataset',
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
                text: 'Upcoming Data Year',
                fontSize:'10',
                position:'top',
                font: {
                    size: 10
                },
                color:'white'
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
                    color:'white'
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
        type:'doughnut',
        data:data,
        options:options,
        plugins: [ChartDataLabels]
    }
  
    const myChart = new Chart(
      document.getElementById('graph-upcoming-year'),
      config
    );

}


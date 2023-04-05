// // Add this JavaScript code to your HTML template or a separate .js file

// // Fetch data from your API
// fetch('/my_api/?city=<city>&region=<region>')
// .then(response => response.json())
// .then(data => {
//     // Get the plot1 and plot2 data from the API response
//     const plot1Data = data.plot1;
//     const plot2Data = data.plot2;

//     // Create a bar chart using Chart.js
//     new Chart('bar-chart', {
//         type: 'bar',
//         data: {
//             labels: ['High', 'Medium', 'Low'],
//             datasets: [
//                 {
//                     label: 'Plot1 Data',
//                     data: [plot1Data.high, plot1Data.medium, plot1Data.low],
//                     backgroundColor: 'rgba(75, 192, 192, 0.2)',  // Set the color for the bars
//                     borderColor: 'rgba(75, 192, 192, 1)',  // Set the color for the bar borders
//                     borderWidth: 1  // Set the width of the bar borders
//                 },
//                 {
//                     label: 'Plot2 Data',
//                     data: [plot2Data.authentic, plot2Data.nonauthentic],
//                     backgroundColor: 'rgba(255, 99, 132, 0.2)',  // Set the color for the bars
//                     borderColor: 'rgba(255, 99, 132, 1)',  // Set the color for the bar borders
//                     borderWidth: 1  // Set the width of the bar borders
//                 }
//             ]
//         },
//         options: {
//             responsive: true,
//             scales: {
//                 y: {
//                     beginAtZero: true
//                 }
//             }
//         }
//     });
// })
// .catch(error => console.error('Error:', error));


class CityPageView extends TemplateView {
    // ...

    // Add this method to update the bar chart with data from API
    updateBarChart() {
        // Fetch data from API
        fetch('/my_api/?city=<city>&region=<region>')
        .then(response => response.json())
        .then(data => {
            // Get the plot1 and plot2 data from the API response
            const plot1Data = data.plot1;
            const plot2Data = data.plot2;

            // Update the bar chart data and labels
            this.chart.data.labels = ['High', 'Medium', 'Low'];
            this.chart.data.datasets[0].data = [plot1Data.high, plot1Data.medium, plot1Data.low];
            this.chart.data.datasets[1].data = [plot2Data.authentic, plot2Data.nonauthentic];

            // Update the chart
            this.chart.update();
        })
        .catch(error => console.error('Error:', error));
    }

    // Add this method to create the bar chart
    createBarChart() {
        // Create a bar chart using Chart.js
        this.chart = new Chart('bar-chart', {
            type: 'bar',
            data: {
                labels: ['High', 'Medium', 'Low'],
                datasets: [
                    {
                        label: 'Plot1 Data',
                        data: [],
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',  // Set the color for the bars
                        borderColor: 'rgba(75, 192, 192, 1)',  // Set the color for the bar borders
                        borderWidth: 1  // Set the width of the bar borders
                    },
                    {
                        label: 'Plot2 Data',
                        data: [],
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',  // Set the color for the bars
                        borderColor: 'rgba(255, 99, 132, 1)',  // Set the color for the bar borders
                        borderWidth: 1  // Set the width of the bar borders
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Add this method to initialize the view and create the bar chart
    initialize() {
        this.createBarChart();
        this.updateBarChart();
    }
}

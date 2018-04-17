import { copy } from '@ember/object/internals';
import { inject as service } from '@ember/service';
import Component from '@ember/component';
import stockData from '../dummydata/stock';
import Ember from 'ember';


export default Component.extend({
  dynamicChart: service('dynamic-chart'),
  ajax: Ember.inject.service(),

  chartOptions: {
    rangeSelector: {
      selected: 1
    },
    title: {
      text: 'BTC-USD Live Data'
    }
  },

  actions: {
    setFromServer() {
      this.get('ajax').request("http://0.0.0.0:5000/tf_api/historical_data/historical", {
        headers: {'Accept': 'application/json'},
        method: 'GET',
        data: {
          max_points: 100,
          offset: 935797

        },
      }).then(data => this.set('chartData', generateArray(data)))

        },

    updateSeriesData() {

      let newChartData = this.get('dynamicChart').updateSeriesData(stockData, 100, 514);
      console.log(newChartData);
      this.set('chartData', newChartData);
    },

    setSeriesCount(numSeries) {
      let newChartData = this.get('dynamicChart').updateSeriesCount(stockData, numSeries);
      this.set('chartData', newChartData);
    }
  }
});

function generateArray(series) {
  let newArray = [];
  series.forEach((element) => {
    let date = new Date(element.ts);
    newArray.push([date.getTime(), element.price])
  });

  return [{
    name: 'BTC',
    data: newArray
  }]
}

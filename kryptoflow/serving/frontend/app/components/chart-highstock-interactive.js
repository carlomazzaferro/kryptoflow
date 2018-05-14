import { copy } from '@ember/object/internals';
import { inject as service } from '@ember/service';
import Component from '@ember/component';
import Ember from 'ember';
import EmberHighChartsComponent from 'ember-highcharts/components/high-charts';


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
  socketIOService: service('socket-io'),
  socketRef: null,
  value: false,
  cachedChartData: [],

  onConnect() {
    console.log('CONNECTED');
  },

  onMessage(data) {
    let date = new Date(data.ts);
    let ct = copy(this.get('chartData'));
    ct[0].data.push([date.getTime(), data.price]);
    this.set('chartData', ct);
  },

  actions: {

    setFromServer() {
      this.get('ajax').request("http://0.0.0.0:5000/tf_api/historical_data/historical", {
        headers: {'Accept': 'application/json'},
        method: 'GET',
        data: {
          max_points: 100,
          offset: 1392000

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
    },

    buttonStart() {
      if (this.value === false) {
        this.set('value', true);
        const socket = this.get('socketIOService').socketFor('http://0.0.0.0:5000/');
        console.log(socket);
        console.log(this.value);

        this.socketRef = socket;
        socket.on('connect', this.onConnect, this);
        socket.on('price_event', this.onMessage, this);
      }

      else  {
        this.set('value', false);

        this.get('socketIOService').closeSocketFor('http://0.0.0.0:5000/');

        console.log('livestream interrupted');
        console.log('state' + this.value);

        this.socketRef = null;
      }

    },
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

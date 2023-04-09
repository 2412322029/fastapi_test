<template>
    <div id="lineChart"  style="width:1000px;height: 400px;"></div>
</template>

<script setup lang="ts">
import { OpenAPI } from "@/client";
import { barChart } from "@/script/chart.ts";
import { lineChart } from "@/script/chart.ts";
import { onMounted } from "vue";

var chartOption = {
    title: "状态",
    type: "verticle",
    xAxis: {
        data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    },
    yAxis: {
        tofixed: 0,
        type: 'value',
        tag: "%",
    },
    series: [{
        name: 'cpu',
        data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        type: 'area',
        tag: "s",
    },
    {
        name: 'memory',
        data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        type: 'area',
        tag: "s",
    }]
};

onMounted(() => {
    var linechart = new lineChart("lineChart", chartOption);
    console.log(linechart)
    const ws = new WebSocket(`${OpenAPI.BASE.replace('http', 'ws')}/api/websocket/cpu`)
    ws.addEventListener("message", (ev) => {
        try {
            var myDate = new Date();
            linechart.context.clearRect(0, 0, 20000, 20000)
            let cp = JSON.parse(ev.data)
            linechart.series[1]['data'].shift()
            linechart.series[1]['data'].push(cp['cpu'])
            linechart.series[2]['data'].shift()
            linechart.series[2]['data'].push(Math.floor(cp['memory']['used']/cp['memory']['total']*1000)/10)
            linechart.xAxis['data'].shift()
            linechart.xAxis['data'].push(myDate.toLocaleString().split(':')[2])
            linechart.draw()
        } catch (e) {
            console.log(e)
        }

    })
})



</script>
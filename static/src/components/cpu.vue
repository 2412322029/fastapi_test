<template>
    <div id="lineChart" style="width:80%;"></div>
    内存:{{ Math.floor(mem[0] / 1024 ** 3 * 100) / 100 }}/{{ Math.floor(mem[1] / 1024 ** 3 * 100) / 100 }} (GB)
</template>

<script setup lang="ts">
import { OpenAPI } from "@/client";
import { lineChart } from "@/script/chart.ts";
import { onMounted, ref } from "vue";
import { useMessage } from 'naive-ui'
const message = useMessage()
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
const mem = ref([0, 0])
onMounted(() => {
    var linechart = new lineChart("lineChart", chartOption);
    console.log(linechart)
    const ws = new WebSocket(`${OpenAPI.BASE.replace('http', 'ws')}/api/websocket/cpu`)
    ws.addEventListener("error", (ev) => {
        message.error('websocket connection error')
    })
    ws.addEventListener("open", (ev) => {
        message.success('websocket ready')
    })
    ws.addEventListener("close", (ev) => {
        message.error('websocket close')
    })
    ws.addEventListener("message", (ev) => {
        try {
            var myDate = new Date();
            linechart.context.clearRect(0, 0, 20000, 20000)
            let cp = JSON.parse(ev.data)
            linechart.series[1]['data'].shift()
            linechart.series[1]['data'].push(cp['cpu'])
            linechart.series[2]['data'].shift()
            mem.value = [cp['memory']['used'], cp['memory']['total']]
            linechart.series[2]['data'].push(Math.floor(cp['memory']['used'] / cp['memory']['total'] * 1000) / 10)
            linechart.xAxis['data'].shift()
            linechart.xAxis['data'].push(myDate.toLocaleString().split(':')[2])
            linechart.draw()
        } catch (e) {
            console.log(e)
        }

    })
})



</script>
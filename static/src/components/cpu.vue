<template>
    <div id="lineChart" style="width:100%; height: 300px;"></div>
    内存:{{ Math.floor(mem[0] / 1024 ** 3 * 100) / 100 }}/{{ Math.floor(mem[1] / 1024 ** 3 * 100) / 100 }} (GB)
    <br>
    磁盘:{{ disk }} (GB)
</template>

<script setup lang="ts">
import { OpenAPI, Service } from "@/client";
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
const disk = ref()
const daw = () => {
    var linechart = new lineChart("lineChart", chartOption);
    Service.getCpu().then((ev) => {
        try {
            var myDate = new Date();
            linechart.context.clearRect(0, 0, 20000, 20000)
            linechart.series[1]['data'].shift()
            linechart.series[1]['data'].push(ev.cpu)
            linechart.series[2]['data'].shift()
            mem.value = [ev['memory']['used'], ev['memory']['total']]
            linechart.series[2]['data'].push(Math.floor(ev['memory']['used'] / ev['memory']['total'] * 1000) / 10)
            linechart.xAxis['data'].shift()
            linechart.xAxis['data'].push(myDate.toLocaleString().split(' ')[1])
            linechart.draw()
        } catch (e) {
            console.log(e)
        }
    })
}
const start = () => {
    daw()
    //@ts-ignore
    setInterval(() => {
        daw()
    }, 5000)

    Service.getDisk().then((ev) => {
        disk.value = Math.floor(ev.disk.used / 1024 ** 3 * 100) / 100 + '/' + Math.floor(ev.disk.total / 1024 ** 3 * 100) / 100

    })
}
onMounted(() => {
    start()
})



</script>
const ctx = document.getElementById("lineChart")
const currentPointInput = document.getElementById("current-point")
const monthlyGetPointInput = document.getElementById("monthly-get-point")
const goalPointInput = document.getElementById("goal-point")


const getAdjustedMonth = (month) => {
    return ((month - 1) % 12) + 1;
}

const updateBarChart = () => { 
    const currentPoint = currentPointInput.value;
    const monthlyPoint = monthlyGetPointInput.value;

    // 頭文字が0の場合は処理を終了
    if (currentPoint.match(/^([1-9][0-9]*|0)$/) === null || monthlyPoint.match(/^([1-9][0-9]*|0)$/) === null) {
        return;
    }

    myLineChart.data.datasets[0].data = [0, 0, 0, 0, 0].map((val, idx) => {
        let updateVal = 0;
        switch (idx) {
        case 0:
            updateVal = Number(currentPoint)
            break
        case 1:
            updateVal = Number(monthlyPoint) * 1 + Number(currentPoint)
            break    
        case 2:
            updateVal = Number(monthlyPoint) * 3 + Number(currentPoint)
            break
        case 3:
            updateVal = Number(monthlyPoint) * 6 + Number(currentPoint)
            break
        default:
            updateVal = Number(monthlyPoint) * 12 + Number(currentPoint)
            break   
        }
        return updateVal
    })
    myLineChart.update()
}

const updateLineChart = () => { 
    const goalPoint = goalPointInput.value;
    // 頭文字が0の場合は処理を終了
    if (goalPoint.match(/^([1-9][0-9]*|0)$/) === null) {
        return;
    }
    myLineChart.options.annotation.annotations[0].value  =  Number(goalPoint);
    myLineChart.options.annotation.annotations[0].endValue  =  Number(goalPoint);
    myLineChart.update()
}

const updateLink = () => {
    // 入力された目標ポイント数を取得
    const goalPoint = document.getElementById('goal-point').value;
    // リンクのhrefを更新
    const link = document.getElementById('exchange-link');

    // 現在のパスを取得
    const currentPath = window.location.pathname;

    // パスに基づいてリンクを設定
    // デフォルトのパスを/simulation/から/に変更したのでこれで問題ない
    link.href = currentPath + "com_list/?max_points=" + encodeURIComponent(goalPoint);
}

// ページが読み込まれた時と、入力値が変更された時にupdateLink関数を呼び出す
window.onload = function() {
    updateLink();
    document.getElementById('goal-point').addEventListener('input', updateLink);
};

// 月の取得
const today = new Date()
const thisMonth = today.getMonth() + 1

// 初期状態のグラフ
const initPoint = 0
const initPointChart = Array(6).fill(initPoint)
const initGoalPoint = 0

// 今、1、3、半年、1年後

let myLineChart = new Chart(ctx, {
    type: 'bar', // 最初のデフォルトのタイプを設定
    data: {
        labels: [
            "今",
            "1ヶ月後",
            "3ヶ月後",
            "半年後",
            "1年後"
        ],
        datasets: [
        {
            label: '獲得予定ポイント',
            type: 'bar',
            data: initPointChart,
            borderColor: [
                "rgba(255, 219, 32, 1)", // thisMonth
                "rgba(245, 124, 28, 1)", // thisMonth + 1
                "rgba(245, 124, 28, 1)", // thisMonth + 2 (特定の色)
                "rgba(245, 124, 28, 1)", // thisMonth + 3
                "rgba(245, 124, 28, 1)", // thisMonth + 4
                "rgba(245, 124, 28, 1)", // thisMonth + 5
            ],
            backgroundColor: [
                "rgba(255, 219, 32, 1)", // thisMonth
                "rgba(245, 124, 28, 1)", // thisMonth + 1
                "rgba(245, 124, 28, 1)", // thisMonth + 2 (特定の色)
                "rgba(245, 124, 28, 1)", // thisMonth + 3
                "rgba(245, 124, 28, 1)", // thisMonth + 4
                "rgba(245, 124, 28, 1)", // thisMonth + 5
            ],
            borderWidth: 2
        }
        ],
    },
    options: {
        responsive: true, 
        title: {
            display: false,
            text: 'ポイント獲得予定'
        },
        scales: {
            yAxes: [{
            id: 'goal',
            ticks: {
            suggestedMax: 10,
            suggestedMin: 0,
            callback: function(value, index, values){
                return  value +  ''
            }
        }
        }]    
        },
        legend: {
            display: false // ラベルを非表示にする
        },
        annotation: {
            annotations: [
            {
                type: 'line', // 線分を指定
                drawTime: 'afterDatasetsDraw',
                mode: 'horizontal', // 水平を指定
                scaleID: 'goal', // 基準とする軸のid名
                value: initGoalPoint, // 引きたい線の数値（始点）
                endValue: initGoalPoint, // 引きたい線の数値（終点）
                borderColor: 'red', // 線の色
                borderWidth: 3, // 線の幅（太さ）
                label: { // ラベルの設定
                    backgroundColor: 'rgba(255,255,255,0.5)',
                    bordercolor: 'rgba(200,60,60,0.8)',
                    borderwidth: 2,
                    fontStyle: 'bold',
                    fontSize: 10,
                    fontColor: '#616161',
                    xPadding: 4,
                    yPadding: 4,
                    cornerRadius: 3,
                    position: 'center',
                    xAdjust: 50,
                    yAdjust: 0,
                    enabled: true,
                    content: '目標ポイント'
                }
            }]
        }
    }
})

updateBarChart();
updateLineChart();

// inputタグの値が変更されたときに値を表示
currentPointInput.addEventListener("input", () => {


    updateBarChart();

})

monthlyGetPointInput.addEventListener("input", () => { 
    updateBarChart();
})

// 目標ポイントの更新
goalPointInput.addEventListener("input", () => { 
    updateLineChart();
})


'use client'
import React, { useEffect, useState } from 'react'
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts';
const url = process.env.NEXT_PUBLIC_APP_API

const Graph = () => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);
  const [warning, setWarning] = useState(null);

  const getData = async () => {
    setLoading(true);
    await fetch(url)
      .then((json) => json.json())
      .then((response) => {
        if (response.alert) {
          setWarning({ alert: response.alert, time: response.history.at(-1).time, level: response.level })
          // alert(response.alert)
        }
        setData(response.history)
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    getData();
    setInterval(() => {
      console.log('updating...')
      getData();
    }, 10000)
  }, [])

  if (loading) return ('Loading...')

  return (
    <section className='w-full flex flex-col items-center justify-center'>
      <div className='mb-4'>
        {
          warning && (<div className='w-full items-center flex flex-row gap-x-2'>
            <div>
              {warning.time}
            </div>
            <div>
              {warning.alert}
            </div>
            <div>
              ({warning.level.toFixed(2)}%)
            </div>
          </div>)
        }
      </div>
      <LineChart width={1000} height={550} data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
        <Line type="monotone" dataKey="approved" stroke="#8884d8" />
        <Line type="monotone" dataKey="backend_reversed" stroke="#82ca9d" />
        <Line type="monotone" dataKey="denied" stroke="#011627" />
        <Line type="monotone" dataKey="failed" stroke="#FF3366" />
        <Line type="monotone" dataKey="processing" stroke="#20A4F3" />
        <Line type="monotone" dataKey="refunded" stroke="#626D58" />
        <Line type="monotone" dataKey="reversed" stroke="#56282D" />
        <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
        <XAxis dataKey="time" />
        <YAxis />
        <Tooltip />
      </LineChart>
    </section>
  )
}

export default Graph
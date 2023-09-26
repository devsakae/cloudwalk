'use client';
import React, { useState } from 'react'
const url = process.env.NEXT_PUBLIC_APP_API

const Form = () => {
  const [payload, setPayload] = useState({ approved: 0 });

  const sendData = async (e) => {
    e.preventDefault();
    setPayload({})
    await fetch(url, {
      method: "POST",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload)
    }).then((response) => console.log(response.json())).catch((err) => console.error(err));
  }
 
  return (
    <form onSubmit={ (e) => sendData(e) }>
      <label htmlFor='approved'>
        Approved:
        <input
          id="approved"
          name="approved"
          type="number"
          value={ payload.approved }
          onChange={ (e) => setPayload((prev) => ({ ...prev, approved: e.target.value })) }
        />
      </label>
      <button>
        Save this data
      </button>
    </form>
  )
}

export default Form
import React from 'react'

const Info = (props) => {
  return (
    <div className='flex flex-row w-48 justify-between'>
      <div>Approved:</div>
      <div>{ props.info.approved }</div>
    </div>
  )
}

export default Info
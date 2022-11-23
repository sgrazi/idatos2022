import { useState, useEffect } from 'react'

function Main() {
    const [time, setTime] = useState(0)

    useEffect(() => {
        fetch('/time').then(res => res.json()).then(data => {
            setTime(data.time)
        })
    }, [])

    return (
      <div className="App">
        Main content will go here.
        Time is {time}
      </div>
    );
  }
  
  export default Main;
  
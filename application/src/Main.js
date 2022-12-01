import { useState, useEffect } from 'react'
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Search from './Search/SearchBar'

const rows = [
  { name: "movie 1", rating: 5, age_rating: "PG13", services: "Netflix, HBO"},
  { name: "movie 2", rating: 5, age_rating: "PG13", services: "HBO"},
  { name: "movie 3", rating: 5, age_rating: "PG13", services: "HBO"},
  { name: "movie 4", rating: 5, age_rating: "PG13", services: "Amazon Prime"},
  { name: "movie 5", rating: 5, age_rating: "PG13", services: "Disney+, Netflix"},
];

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

        <Search/>

        <TableContainer style={{
          width: "auto",
          padding: 24,
          marginBottom: 50,
          backgroundColor: "#ECECEC"
        }
        } component={Paper}>
          <Table aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>Poster</TableCell>
                <TableCell>Nombre</TableCell>
                <TableCell align="right">Calificacion</TableCell>
                <TableCell align="right">Calificacion de edad</TableCell>
                <TableCell align="right">Servicios</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {rows.map((row) => (
                <TableRow
                  key={row.name}
                >
                  <TableCell> <img src="https://m.media-amazon.com/images/M/MV5BOGJlZGJiN2ItM2VlMi00NWQ5LWJkYzYtMWY2MmJhMTFlNGQ3XkEyXkFqcGdeQXVyMTAyOTE2ODg0._V1_.jpg" alt="" border="3" height="100" width="70"/></TableCell>
                  <TableCell scope="row">{row.name}</TableCell>
                  <TableCell align="right">{row.rating}</TableCell>
                  <TableCell align="right">{row.age_rating}</TableCell>
                  <TableCell align="right">{row.services}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </div>
    );
  }
  
  export default Main;
  
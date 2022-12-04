import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Search from './Search/SearchBar'
import { useEffect, useState } from 'react';

function Main() {
    const [movies, setMovies] = useState([{
      country: "Canada",
      description: "A small fishing village must procure a local doctor to secure a lucrative business contract. When unlikely candidate and big city doctor Paul Lewis lands in their lap for a trial residence, the townsfolk rally together to charm him into staying. As the doctor's time in the village winds to a close, acting mayor Murray French has no choice but to pull out all the stops.",
      duration: "113 min",
      genres: [
        "COMEDY",
        "DRAMA"
      ],
      id: 1,
      platforms: [
        "Amazon Prime Video"
      ],
      release_year: "2014",
      title: "The Grand Seduction"
    }])

    const [rows, setRows] = useState([])

    useEffect(() => {
      setRows(
        movies.map((movie) => {
          return { name: movie.title, description: movie.description, release_year: movie.release_year, duration: movie.duration, services: movie.platforms, genres: movie.genres}
        })
      )
    }
    ,[movies])

    return (
      <div className="App">
        <Search setMovies={setMovies}/>
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
                <TableCell>Título</TableCell>
                <TableCell>Descripcion</TableCell>
                <TableCell align="right">Año</TableCell>
                <TableCell align="right">Duración</TableCell>
                <TableCell>Servicios</TableCell>
                <TableCell>Género</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {rows.map((row) => (
                <TableRow
                  key={row.name}
                >
                  <TableCell> <img src="https://m.media-amazon.com/images/M/MV5BOGJlZGJiN2ItM2VlMi00NWQ5LWJkYzYtMWY2MmJhMTFlNGQ3XkEyXkFqcGdeQXVyMTAyOTE2ODg0._V1_.jpg" alt="" border="3" height="100" width="70"/></TableCell>
                  <TableCell scope="row">{row.name}</TableCell>
                  <TableCell>{row.description}</TableCell>
                  <TableCell align="right">{row.release_year}</TableCell>
                  <TableCell align="right">{row.duration}</TableCell>
                  <TableCell>{row.services}</TableCell>
                  <TableCell>{row.genres}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </div>
    );
  }
  
  export default Main;
  
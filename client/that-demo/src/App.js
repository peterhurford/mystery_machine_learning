import React, { useState, useEffect } from "react";
import axios from "axios";
import * as url from "./mystery_machine.png";
import Shaggy from "./scooby-doo-characters/Shaggy_Rogers.png";
import Fred from "./scooby-doo-characters/Fred_Jones.png";
import Daphne from "./scooby-doo-characters/Daphne_Blake.png";
import Velma from "./scooby-doo-characters/Velma_Dinkley.png";
import Scooby from "./scooby-doo-characters/Scooby_Doo.png";
import "./App.css";

const images = {
  "Shaggy Rogers": Shaggy,
  "Velma Dinkley": Velma,
  "Fred Jones": Fred,
  "Daphne Blake": Daphne,
  "Scooby-Doo": Scooby
};

function App() {
  const [data, setData] = useState();
  const [textToPredict, setTextToPredict] = useState();
  const [explanations, setExplanation] = useState();

  /**
   * This function makes our api calls. We could attach it to a
   * button but it's way cooler to make them happen in real time
   * using `useEffect` below.
   */
  function predictWhoSaidIt() {
    axios
      .post("/predict", {
        text: textToPredict
      })
      .then(res => {
        setData(res.data);
        console.log(res.data);
      });
    axios
      .post("/explain", {
        text: textToPredict
      })
      .then(res => {
        setExplanation(res.data.explanation);
        console.log(res.data.explanation);
      });
  }

  /**
   * This effect says: "whenever the `textToPredict` changes(and if
   * it exists), run our function `predictWhoSaidIt()`"
   */
  useEffect(() => {
    if (textToPredict) {
      predictWhoSaidIt();
    }
  }, [textToPredict]);

  return (
    <div className="App">
      <header className="App-header">
        <div className="header">
          Mystery Machine Learning!
          <img src={url} className="App-logo" alt="logo" />
        </div>

        <div className="text-preview">
          Who said : "{!textToPredict ? "___________" : textToPredict}" ?
        </div>
        <textarea
          className="text-area"
          onChange={e => setTextToPredict(e.target.value)}
        />

        {/* <button onClick={predictWhoSaidIt}>Let's find out!</button> */}

        {explanations && (
          <div className="content">
            <PredictionsContainer data={data} />
            <ExplanationsContainer data={data} explanations={explanations} />
          </div>
        )}
      </header>
    </div>
  );
}

function PredictionsContainer({ data }) {
  return (
    <div className="results">
      {data && data.prediction && (
        <div className="winner">
          It was probably...
          <img
            className="winner-image"
            src={images[data.prediction]}
            alt={"winner"}
          />
          {data.prediction}!
        </div>
      )}

      <div className="data-table">
        <table>
          <tbody>
            {data &&
              Object.keys(data.probabilities)
                .map(person => {
                  return {
                    name: person,
                    score: (data.probabilities[person] * 100).toFixed(2)
                  };
                })
                .sort((a, b) => b.score - a.score)
                .map((person, i) => (
                  <tr key={`${person.name}-${i}`}>
                    <td className="person-name">{person.name}</td>
                    <td className="person-score">{person.score} %</td>
                  </tr>
                ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function ExplanationsContainer({ data, explanations }) {
  const [isExplanationTableVisible, toggleExplanationTable] = useState(false);

  /**
   * This function is used for coloring the words in the word breakdown.
   * it takes the response from `/explain`, locates the word from the results
   * and if it exists, colors it depending on whether it is positive or
   * negative and to what degree.  */

  function getWordHeatValue(word) {
    const foundWord = Object.keys(explanations).find(el =>
      word.toLowerCase().includes(el.toLowerCase())
    );
    const value = explanations[foundWord] * 4;
    if (value && value > 0) {
      return { color: `rgba(0, 255, 0, ${value})` };
    } else if (value && value < 0) {
      return { color: `rgba(255, 0, 0, ${Math.abs(value)})` };
    }
    return { color: "rgba(255, 255, 255, .1)" };
  }

  return (
    data && (
      <div className="explanation">
        <div
          className="explanation-header"
          onClick={() => toggleExplanationTable(!isExplanationTableVisible)}
        >
          Word breakdown:{" "}
        </div>
        {data.text.split(" ").map(word => {
          return (
            <span style={getWordHeatValue(word)} title={explanations[word]}>
              {word + " "}
            </span>
          );
        })}
        <div className="data-table">
          {isExplanationTableVisible && (
            <table>
              <tbody>
                {explanations &&
                  Object.keys(explanations)
                    .map(word => {
                      return {
                        name: word,
                        score: (explanations[word] * 100).toFixed(2)
                      };
                    })
                    .sort((a, b) => b.score - a.score)
                    .map((word, i) => (
                      <tr key={`${word.name}-${i}`}>
                        <td className="person-name">{word.name}</td>
                        <td className="person-score">
                          {word.score > 0 ? `+${word.score}` : word.score}{" "}
                        </td>
                      </tr>
                    ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    )
  );
}

export default App;

package bot

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"regexp"
	"strconv"
	"time"

	"github.com/bwmarrin/discordgo"
)

const URL string = "https://api.openweathermap.org/data/2.5/weather?"


type WeatherData struct {
	Weather []struct {
		Description string `json:"description"`
	} `json:"weather"`
	Main struct {
		Temp     float64 `json:"temp"`
		Humidity int     `json:"humidity"`
	} `json:"main"`
	Wind struct {
		Speed float64 `json:"speed"`
	} `json:"wind"`
	Name string `json:"name"`
}

func getCurrentWeather(message string) *discordgo.MessageSend {
	// Match 5-digit US ZIP code
	r, _ := regexp.Compile(`\d{5}`)
	zip := r.FindString(message)

	// If ZIP not found, return an error
	if zip == "" {
		return &discordgo.MessageSend{
			Content: "Sorry that ZIP code doesn't look right",
		}
	}

	// Build full URL to query OpenWeather
	weatherURL := fmt.Sprintf("%szip=%s&units=imperial&appid=%s", URL, zip, OpenWeatherToken)

	// Create new HTTP client & set timeout
	client := http.Client{Timeout: 5 * time.Second}

	// Query OpenWeather API
	response, err := client.Get(weatherURL)
	if err != nil {
		return &discordgo.MessageSend{
			Content: "Sorry, there was an error trying to get the weather",
		}
	}

	// Open HTTP response body
	body, _ := ioutil.ReadAll(response.Body)
	defer response.Body.Close()

	// Convert JSON
	var data WeatherData
	json.Unmarshal([]byte(body), &data)

	// Pull out desired weather info & Convert to string if necessary
	city := data.Name
	conditions := data.Weather[0].Description
	temperature := strconv.FormatFloat(data.Main.Temp, 'f', 2, 64)
	humidity := strconv.Itoa(data.Main.Humidity)
	wind := strconv.FormatFloat(data.Wind.Speed, 'f', 2, 64)

	// Build Discord embed response
	embed := &discordgo.MessageSend{
		Embeds: []*discordgo.MessageEmbed{{
			Type:        discordgo.EmbedTypeRich,
			Title:       "Current Weather",
			Description: "Weather for " + city,
			Fields: []*discordgo.MessageEmbedField{
				{
					Name:   "Conditions",
					Value:  conditions,
					Inline: true,
				},
				{
					Name:   "Temperature",
					Value:  temperature + "°F",
					Inline: true,
				},
				{
					Name:   "Humidity",
					Value:  humidity + "%",
					Inline: true,
				},
				{
					Name:   "Wind",
					Value:  wind + " mph",
					Inline: true,
				},
			},
		},
		},
	}

	return embed
}

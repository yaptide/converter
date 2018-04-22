package setup

import (
	"encoding/json"
	"fmt"

	"github.com/yaptide/converter/log"
)

var predefinedScoringTypes = map[string]bool{
	"dose":       true,
	"energy":     true,
	"fluence":    true,
	"avg_energy": true,
	"avg_beta":   true,
	"spc":        true,
	"alanine":    true,
	"counter":    true,
	"ddd":        true,
	"crossflu":   true,
}

// TODO: write test checking if all values are assigned
// TODO: not sure about that
var letScoringTypes = map[string]bool{
	"letflu": true,
	"dlet":   true,
	"tlet":   true,
}

// ScoringType ...
type ScoringType interface{}

// DetectorScoring ...
type DetectorScoring struct {
	ScoringType
}

// PredefinedScoring ...
type PredefinedScoring string

// Validate ...
func (s PredefinedScoring) Validate() error {
	_, exists := predefinedScoringTypes[(string(s))]
	if !exists {
		return E{"type": fmt.Errorf("%v is not predefined scoring type", s)}
	}
	return nil
}

// LetTypeScoring ...
type LetTypeScoring struct {
	Type     string     `json:"type"`
	Material MaterialID `json:"material"`
}

// Validate ...
func (s LetTypeScoring) Validate() error {
	result := E{}
	_, exists := letScoringTypes[s.Type]
	if !exists {
		result["type"] = fmt.Errorf("%v is not let scoring type", s.Type)
	}
	if err := s.Material.Validate(); err != nil {
		result["material"] = err
	}
	return result
}

// MarshalJSON json.Marshaller implementation.
func (s PredefinedScoring) MarshalJSON() ([]byte, error) {
	return json.Marshal(struct {
		Type string `json:"type"`
	}{
		Type: string(s),
	})
}

// MarshalJSON json.Marshaller implementation.
func (s LetTypeScoring) MarshalJSON() ([]byte, error) {
	type Alias LetTypeScoring
	return json.Marshal(struct {
		Alias
	}{
		Alias: (Alias)(s),
	})
}

// MarshalJSON ...
func (s DetectorScoring) MarshalJSON() ([]byte, error) {
	return json.Marshal(s.ScoringType)
}

// UnmarshalJSON ...
func (s *DetectorScoring) UnmarshalJSON(b []byte) error {
	var scoring struct {
		Type string `json:"type"`
	}
	getTypeErr := json.Unmarshal(b, &scoring)
	if getTypeErr != nil {
		return getTypeErr
	}

	log.Error(scoring.Type)
	_, isPredefined := predefinedScoringTypes[scoring.Type]
	if isPredefined {
		s.ScoringType = PredefinedScoring(scoring.Type)
		return nil
	}

	_, isLet := letScoringTypes[scoring.Type]
	if isLet {
		var detectorScoring LetTypeScoring
		if err := json.Unmarshal(b, &detectorScoring); err != nil {
			return err
		}
		s.ScoringType = detectorScoring
		return nil
	}

	return fmt.Errorf("unknown scoring type")
}

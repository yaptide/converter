package setup

import (
	"encoding/json"
	"fmt"
)

var predefinedParticleTypes = map[string]bool{
	"neutron":          true,
	"proton":           true,
	"pion_pi_minus":    true,
	"pion_pi_plus":     true,
	"pion_pi_zero":     true,
	"he_3":             true,
	"he_4":             true,
	"anti_neutron":     true,
	"anti_proton":      true,
	"kaon_minus":       true,
	"kaon_plus":        true,
	"kaon_zero":        true,
	"kaon_anti":        true,
	"gamma":            true,
	"electron":         true,
	"positron":         true,
	"muon_minus":       true,
	"muon_plus":        true,
	"e_neutrino":       true,
	"e_anti_neutrino":  true,
	"mi_neutrino":      true,
	"mi_anti_neutrino": true,
	"deuteron":         true,
	"triton":           true,
}

// ParticleType ...
type ParticleType interface {
	Validate() error
}

// Particle is interface for particle scored in detectors.
type Particle struct {
	ParticleType
}

// AllParticles ...
type AllParticles string

// Validate ...
func (p AllParticles) Validate() error {
	return nil
}

// PredefinedParticle ...
type PredefinedParticle string

// Validate ...
func (p PredefinedParticle) Validate() error {
	_, exists := predefinedParticleTypes[string(p)]
	if !exists {
		return fmt.Errorf("%v is not a predefined particle type", p)
	}
	return nil
}

// HeavyIon ...
type HeavyIon struct {
	Charge        int64 `json:"charge"`
	NucleonsCount int64 `json:"nucleonsCount"`
}

// Validate ...
func (p HeavyIon) Validate() error {
	result := E{}
	if p.Charge <= 2 {
		result["charge"] = fmt.Errorf("Number of protons must be larger than 2")
	}
	if p.Charge > p.NucleonsCount && p.NucleonsCount > 0 {
		result["charge"] = fmt.Errorf("Number of protons can't be larger than number of nucleons")
	}
	if p.NucleonsCount <= 0 {
		result["nucleonsCount"] = fmt.Errorf("Number of nucleons must be larger than 0")
	}
	return result
}

// MarshalJSON json.Marshaller implementation.
func (p PredefinedParticle) MarshalJSON() ([]byte, error) {
	return json.Marshal(struct {
		Type string `json:"type"`
	}{
		Type: string(p),
	})
}

// MarshalJSON ...
func (p AllParticles) MarshalJSON() ([]byte, error) {
	return json.Marshal(struct {
		Type string `json:"type"`
	}{
		Type: "all",
	})
}

// MarshalJSON json.Marshaller implementation.
func (p HeavyIon) MarshalJSON() ([]byte, error) {
	type Alias HeavyIon
	return json.Marshal(struct {
		Type string `json:"type"`
		Alias
	}{
		Type:  "heavy_ion",
		Alias: Alias(p),
	})
}

// MarshalJSON ...
func (p Particle) MarshalJSON() ([]byte, error) {
	return json.Marshal(p.ParticleType)
}

// UnmarshalJSON ...
func (p *Particle) UnmarshalJSON(b []byte) error {
	var rawParticle struct {
		Type string `json:"type"`
	}
	if err := json.Unmarshal(b, &rawParticle); err != nil {
		return err
	}
	switch rawParticle.Type {
	case "all":
		p.ParticleType = AllParticles("all")
	case "heavy_ion":
		var heavyIon HeavyIon
		if err := json.Unmarshal(b, &heavyIon); err != nil {
			return err
		}
		p.ParticleType = heavyIon
	default:
		_, isPredefined := predefinedParticleTypes[rawParticle.Type]
		if !isPredefined {
			return fmt.Errorf("unknown particle type")
		}
		p.ParticleType = PredefinedParticle(rawParticle.Type)
	}
	return nil
}

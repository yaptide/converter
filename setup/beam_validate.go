package setup

import (
	"fmt"

	"github.com/yaptide/converter/validate"
)

// Validate ...
func (b Beam) Validate() error {
	result := E{}

	if err := b.Direction.Validate(); err != nil {
		result["direction"] = err
	}
	if err := b.Divergence.Validate(); err != nil {
		result["divergence"] = err
	}
	if err := b.Particle.Validate(); err != nil {
		result["particleType"] = err
	}

	if b.InitialBaseEnergy < 0 {
		result["initialBaseEnergy"] = fmt.Errorf("shuld be positive value")
	}

	if b.InitialEnergySigma < 0 {
		result["initialEnergySigma"] = fmt.Errorf("should be positive value")
	}

	return result
}

// Validate ...
func (b BeamDirection) Validate() error {
	result := E{}

	if err := validate.InRange2PI(b.Phi); err != nil {
		result["phi"] = err
	}
	if err := validate.InRangePI(b.Theta); err != nil {
		result["theta"] = err
	}

	if len(result) > 0 {
		return result
	}
	return nil
}

// Validate ...
func (b BeamDivergence) Validate() error {
	result := E{}

	// TODO research this better;
	return result
}

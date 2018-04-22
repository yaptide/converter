package setup

import (
	"encoding/json"

	"github.com/yaptide/converter/geometry"
	"github.com/yaptide/converter/validate"
)

// DetectorCylinder is detector with cylindrical shape directed along z-axis.
type DetectorCylinder struct {
	Radius geometry.Range               `json:"radius"`
	Angle  geometry.Range               `json:"angle"`
	ZValue geometry.Range               `json:"zValue"`
	Slices geometry.Vec3DCylindricalInt `json:"slices"`
}

// Validate ...
func (d DetectorCylinder) Validate() error {
	result := E{}

	if err := d.Radius.ValidatePositive(); err != nil {
		result["radius"] = err
	}

	if err := d.Angle.ValidateFunc(validate.InRange2PI); err != nil {
		result["angle"] = err
	}

	if err := d.ZValue.Validate(); err != nil {
		result["zValue"] = err
	}

	if len(result) > 0 {
		return result
	}
	return nil
}

// MarshalJSON json.Marshaller implementation.
func (d DetectorCylinder) MarshalJSON() ([]byte, error) {
	type Alias DetectorCylinder
	return json.Marshal(struct {
		Type string `json:"type"`
		Alias
	}{
		Type:  detectorGeometryType.cylinder,
		Alias: Alias(d),
	})
}

package setup

import (
	"encoding/json"

	"github.com/yaptide/converter/geometry"
)

// DetectorMesh detector.
type DetectorMesh struct {
	Center geometry.Point    `json:"center"`
	Size   geometry.Vec3D    `json:"size"`
	Slices geometry.Vec3DInt `json:"slices"`
}

// Validate ...
func (d DetectorMesh) Validate() error {
	result := E{}

	if err := d.Size.ValidatePositive(); err != nil {
		result["size"] = err
	}

	if err := d.Slices.ValidatePositive(); err != nil {
		result["slices"] = err
	}

	if len(result) > 0 {
		return result
	}
	return nil
}

// MarshalJSON json.Marshaller implementation.
func (d DetectorMesh) MarshalJSON() ([]byte, error) {
	type Alias DetectorMesh
	return json.Marshal(struct {
		Type string `json:"type"`
		Alias
	}{
		Type:  detectorGeometryType.mesh,
		Alias: Alias(d),
	})
}

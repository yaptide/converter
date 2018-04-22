package setup

import (
	"encoding/json"

	"github.com/yaptide/converter/geometry"
)

// DetectorGeomap detector used to debug geometry.
type DetectorGeomap struct {
	Center geometry.Point    `json:"center"`
	Size   geometry.Vec3D    `json:"size"`
	Slices geometry.Vec3DInt `json:"slices"`
}

// Validate ...
func (d DetectorGeomap) Validate() error {
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
func (d DetectorGeomap) MarshalJSON() ([]byte, error) {
	type Alias DetectorGeomap
	return json.Marshal(struct {
		Type string `json:"type"`
		Alias
	}{
		Type:  detectorGeometryType.geomap,
		Alias: Alias(d),
	})
}

package setup

import (
	"encoding/json"
	"fmt"

	"github.com/yaptide/converter/geometry"
)

// SphereBody represent sphere with given radius in space.
type SphereBody struct {
	Center geometry.Point `json:"center"`
	Radius float64        `json:"radius"`
}

// Validate ...
func (b SphereBody) Validate() error {
	result := E{}

	if b.Radius <= 0 {
		result["radius"] = fmt.Errorf("should be positive non-zero value")
	}

	if len(result) > 0 {
		return result
	}
	return nil
}

// MarshalJSON json.Marshaller implementation.
func (b SphereBody) MarshalJSON() ([]byte, error) {
	type Alias SphereBody
	return json.Marshal(struct {
		Type string `json:"type"`
		Alias
	}{
		Type:  bodyType.sphere,
		Alias: Alias(b),
	})
}

// CuboidBody represent cuboid of given sizes in a space.
type CuboidBody struct {
	Center geometry.Point `json:"center"`
	Size   geometry.Vec3D `json:"size"`
}

// Validate ...
func (b CuboidBody) Validate() error {
	result := E{}

	if err := b.Size.ValidatePositive(); err != nil {
		result["size"] = err
	}

	if len(result) > 0 {
		return result
	}
	return nil
}

// MarshalJSON json.Marshaller implementation.
func (b CuboidBody) MarshalJSON() ([]byte, error) {
	type Alias CuboidBody
	return json.Marshal(struct {
		Type string `json:"type"`
		Alias
	}{
		Type:  bodyType.cuboid,
		Alias: Alias(b),
	})
}

// CylinderBody represent cylinder of given sizes in a space.
type CylinderBody struct {
	Center geometry.Point `json:"baseCenter"`
	Height float64        `json:"height"`
	Radius float64        `json:"radius"`
}

func (b CylinderBody) Validate() error {
	result := E{}

	if b.Height <= 0 {
		result["height"] = fmt.Errorf("should positive non-zero value")
	}
	if b.Height <= 0 {
		result["radius"] = fmt.Errorf("should positive non-zero value")
	}

	if len(result) > 0 {
		return result
	}
	return nil
}

// MarshalJSON json.Marshaller implementation.
func (b CylinderBody) MarshalJSON() ([]byte, error) {
	type Alias CylinderBody
	return json.Marshal(struct {
		Type string `json:"type"`
		Alias
	}{
		Type:  bodyType.cylinder,
		Alias: Alias(b),
	})
}

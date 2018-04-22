package setup

import (
	"encoding/json"
	"fmt"
)

// MaterialVoxel TODO
type MaterialVoxel struct {
	_ int // mock to fix memory alignment issue.
}

// Validate ...
func (m MaterialVoxel) Validate() error {
	return fmt.Errorf("not implemented")
}

// MarshalJSON json.Marshaller implementation.
func (v MaterialVoxel) MarshalJSON() ([]byte, error) {
	type Alias MaterialVoxel
	return json.Marshal(struct {
		Type string `json:"type"`
		Alias
	}{
		Type:  materialType.voxel,
		Alias: (Alias)(v),
	})
}

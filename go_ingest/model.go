package main

import (
  "database/sql"
  "fmt"
)
// swagger:parameters admin addCompany
type queryD struct {
  //  id of the entry
  //  in: int64
  ID     int     `json:"id" example:1`
  //  action: SQL between SELECT and FROM
  //  in: string
  Action string  `json:"action" example: name,price`
  //  table: name of the table
  //  in: string
  Table  string  `json:"table" example: product` 
  //  filter: additional filters after table name
  //  in: string
  Filter string  `json:"filter" example: WHERE id = 1`
}
type resD struct {
  Line string `json:line`
} 
func (p *queryD) getEntry(db *sql.DB) ([]map[string]interface{}, error)  {
  list := make([]map[string]interface{}, 0)
  queryS := "SELECT " + p.Action + " FROM " + p.Table + " " + p.Filter + ";"
  //   rows, err := db.Query("select 1; select 2") // injest test
  //   fmt.Println(rows)  
  rows, err := db.Query(queryS)
  if err != nil {
    return list, fmt.Errorf("Failed selecting from table: %v", err)
  }
  cols, _ := rows.Columns()
  defer rows.Close()
	for rows.Next() {
    vals := make([]interface{}, len(cols))
    for i, _ := range cols {
        var s string
        vals[i] = &s
    }
    err = rows.Scan(vals...)
    if err != nil {
      return list, fmt.Errorf("Failed selecting from table: %v", err)
    }
    m := make(map[string]interface{})
    for i, val := range vals {m[cols[i]] = val}
    list = append(list, m)
	}
  return list, nil
}
func (p *queryD) updateEntry(db *sql.DB) error {
  queryS := "UPDATE " + p.Table + " SET " + p.Action + " " + p.Filter + ";"
  _, err := db.Exec(queryS)
  return err
}
func (p *queryD) deleteEntry(db *sql.DB) error {
  queryS := "DELETE FROM " + p.Table + " " + p.Filter + ";"
  // fmt.Println(queryS)
  _, err := db.Exec(queryS)
  return err
}
func (p *queryD) createEntry(db *sql.DB) error {
  queryS := "INSERT INTO " + p.Table + p.Action + " " + p.Filter + ";"
  _, err := db.Exec(queryS)
  return err
}

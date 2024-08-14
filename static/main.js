define(['base/js/namespace', 'base/js/events'], function(Jupyter, events) {
    function load_ipython_extension() {
        const dependencies = {};

        function update_dependencies(cell) {
            const code = cell.get_text();
            const cellIndex = Jupyter.notebook.find_cell_index(cell);

            fetch('/api/code_dependencies', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code: code }),
            })
            .then(response => response.json())
            .then(data => {
                dependencies[cellIndex] = data;
                rerun_dependent_cells(cellIndex);
            });
        }

        function rerun_dependent_cells(cellIndex) {
            const definedVars = dependencies[cellIndex].defined_vars;

            for (let i = cellIndex + 1; i < Jupyter.notebook.ncells(); i++) {
                const cellDeps = dependencies[i];
                if (cellDeps && cellDeps.used_vars.some(v => definedVars.includes(v))) {
                    Jupyter.notebook.execute_cells([i]);
                }
            }
        }

        events.on('execute.CodeCell', function(event, data) {
            const cell = data.cell;
            update_dependencies(cell);
        });

        events.on('notebook_loaded.Notebook', function() {
            Jupyter.notebook.get_cells().forEach((cell, index) => {
                if (cell.cell_type === 'code') {
                    update_dependencies(cell);
                }
            });
        });
    }

    return {
        load_ipython_extension: load_ipython_extension
    };
});

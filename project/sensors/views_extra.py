@login_required
def add_sensor_data(request, sensor_id):
    """Add a manual data point to a sensor"""
    sensor = get_object_or_404(Sensor, pk=sensor_id, owner=request.user)
    
    if request.method == 'POST':
        form = ManualDataEntryForm(request.POST)
        
        if form.is_valid():
            data_point = form.save(commit=False)
            data_point.sensor = sensor
            data_point.save()
            
            messages.success(request, f"Data point added successfully: {data_point.value} {data_point.unit}")
            return redirect('sensors:detail', pk=sensor_id)
    
    # If form invalid or not POST, redirect back to detail page
    return redirect('sensors:detail', pk=sensor_id)

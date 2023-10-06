import matplotlib.pyplot as plt
import numpy as np
import io
# Color blind friendly green and red 
colors = {1: '#56E03A', 2: '#D42F4B', 3: 'gold'}
class DataVisualizer:
    @staticmethod
    def plot_diff_lc(oid, lc_det, lc_nondet):
        """
        Plots the difference light curve for a given object.

        Args:
            oid (str): Object ID.
            lc_det (DataFrame): DataFrame containing detection light curve data.
            lc_nondet (DataFrame): DataFrame containing non-detection light curve data.
        """
        fig, ax = plt.subplots(figsize=(14, 8))
        labels = {1: 'g', 2: 'r'}
        colors = {1: '#56E03A', 2: '#D42F4B'}
        markers = {1: 'o', 2: 's'}
        buffer = io.BytesIO()

        # Loop through the passbands
        for fid in [1, 2]:
            # Plot detections if available
            mask = lc_det.fid == fid
            if np.sum(mask) > 0:
                # Note that the detections index is candid and that we are plotting the psf corrected magnitudes
                ax.errorbar(
                    lc_det[mask].mjd, lc_det[mask].magpsf,
                    yerr=lc_det[mask].sigmapsf, c=colors[fid], fmt=markers[fid], label=labels[fid]
                )

            # Plot non-detections if available and if wanted
            mask = (lc_nondet.fid == fid) & (lc_nondet.diffmaglim > -900)
            if np.sum(mask) > 0:
                # Non-detections index is mjd
                ax.scatter(
                    lc_nondet[mask].mjd, lc_nondet[mask].diffmaglim, c=colors[fid], alpha=0.5,
                    marker='v', label="lim.mag. %s" % labels[fid]
                )

        ax.set_title(f"{oid} diff mag lc")
        ax.set_xlabel("MJD")
        ax.set_ylabel("Difference Magnitude")
        ax.legend()
        ax.set_ylim(ax.get_ylim()[::-1])

        plt.savefig(buffer, format='png')
        buffer.seek(0)

        return buffer.read()
    
    @staticmethod
    def plot_corrLC(oid, LC_det):
        """
        Plots the light curve for a given corrected object.

        Args:
            oid (str): Object ID.
            lc_det (DataFrame): DataFrame containing detection light curve data.
        """
        fig, ax = plt.subplots(figsize = (14, 8))
        labels = {1: 'g', 2: 'r'}
        colors = {1: '#56E03A', 2: '#D42F4B'}
        markers = {1: 'o', 2: 's'}
        buffer = io.BytesIO()

        # loop the passbands
        for fid in [1, 2]:
            
            # plot detections if available
            mask = LC_det.fid == fid
            if np.sum(mask) > 0:
                # note that the detections index is candid and that we are plotting the psf corrected magnitudes
                ax.errorbar(LC_det[mask].mjd, LC_det[mask].magpsf_corr, 
                    yerr = LC_det[mask].sigmapsf_corr_ext, c = colors[fid], fmt=markers[fid], label = labels[fid])
            
                
        ax.set_title(f"{oid} corrected lc")
        ax.set_xlabel("MJD")
        ax.set_ylabel("Apparent magnitude")
        ax.legend()
        ax.set_ylim(ax.get_ylim()[::-1])
        #fig.savefig(f'{oid}.png', dpi=300)

        plt.savefig(buffer, format='png')
        buffer.seek(0)

        return buffer.read()
    @staticmethod
    def plot_folded_light_curve(oid, lc_det, lc_nondet, period):
        fig, ax = plt.subplots(figsize=(14, 8))
        labels = {1: 'g', 2: 'r'}
        colors = {1: '#56E03A', 2: '#D42F4B'}
        markers = {1: 'o', 2: 's'}
        buffer = io.BytesIO()

        # Loop through the passbands
        for fid in [1, 2]:
            # Plot detections if available
            mask_det = lc_det.fid == fid
            mask_nondet = (lc_nondet.fid == fid) & (lc_nondet.diffmaglim > -900)
            
            if np.sum(mask_det) > 0:
                # Ajusta el tiempo utilizando el operador de módulo %
                mjd_det_adjusted = lc_det[mask_det].mjd % period
                mag_det = lc_det[mask_det].magpsf

                # Asegúrate de que mjd_det_adjusted y mag_det tengan la misma longitud
                if len(mjd_det_adjusted) != len(mag_det):
                    # Interpola los datos de magnitud en la misma malla de tiempo que las fechas
                    new_mjd = np.linspace(min(mjd_det_adjusted), max(mjd_det_adjusted), len(mjd_det_adjusted))
                    new_mag = np.interp(new_mjd, mjd_det_adjusted, mag_det)
                    mjd_det_adjusted = new_mjd
                    mag_det = new_mag

                ax.errorbar(
                    mjd_det_adjusted, mag_det,
                    yerr=lc_det[mask_det].sigmapsf, c=colors[fid], fmt=markers[fid], label=labels[fid]
                )

            if np.sum(mask_nondet) > 0:
                # Ajusta el tiempo utilizando el operador de módulo %
                mjd_nondet_adjusted = lc_nondet[mask_nondet].mjd % period
                diffmaglim_nondet = lc_nondet[mask_nondet].diffmaglim
                ax.scatter(
                    mjd_nondet_adjusted, diffmaglim_nondet, c=colors[fid], alpha=0.5,
                    marker='v', label="lim.mag. %s" % labels[fid]
                )

        ax.set_title(f"{oid} lc folded")
        ax.set_xlabel("Phase (period=%.3f)" % period)
        ax.set_ylabel("Difference Magnitude")
        ax.legend()
        ax.set_ylim(ax.get_ylim()[::-1])
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        return buffer.read()
    @staticmethod
    def radar_chart(data,oid):
        """
        Generate a radar chart with specified data.

        Args:
            data (dataframe): A Pandas datraframe containing class names and corresponding probabilities.
            oid (str): ID from the ploted object.

        Returns:
            bytes: The binary content of the generated chart.
        """
        class_names = data['class_name']
        probabilities = data['probability']
        num_categories = len(class_names)
        buffer = io.BytesIO()

        angles = np.linspace(0, 2 * np.pi, num_categories, endpoint=False).tolist()

        # Close the chart
        probabilities = np.append(probabilities, probabilities[0])
        angles = np.append(angles, angles[0])

        # Create the figure with a black background
        fig = plt.figure(figsize=(8, 8), facecolor='black')

        # Create a polar subplot
        ax = fig.add_subplot(111, polar=True)
        ax.yaxis.grid(False)

        max_probability = max(probabilities)

        # Draw the large light gray polygon around the center
        ax.fill(angles, [max_probability] * len(angles), color='lightgray', alpha=0.3, label='Light Gray')
        ax.plot(angles, [max_probability] * len(angles), linewidth=2, linestyle='solid', color='gray')

        # Draw the smaller gray polygon
        ax.fill(angles, [0.5] * len(angles), color='gray', alpha=0.7, label='Small Gray')
        ax.plot(angles, [0.5] * len(angles), linewidth=2, linestyle='solid', color='darkgray')

        # Draw the red polygon on the radii
        ax.fill(angles, probabilities, color='red', alpha=0.5, label='Radii')

        # Configure white radial lines
        ax.plot(angles, probabilities, linewidth=2, linestyle='solid', color='red')

        # Set white labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(class_names, color='white')
        ax.set_yticklabels([])

        ax.set_facecolor('black')

        ax.set_title(f"{oid} Probabilities")
        ax.set_xlabel("Probabilities")

        plt.savefig(buffer, format='png')
        buffer.seek(0)

        return buffer.read()
        